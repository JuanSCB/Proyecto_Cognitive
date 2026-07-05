from flask_restx import Namespace, Resource, fields
from flask import request
import requests
import unicodedata
from app.models.salon import Salon
from app.services.ai_service import AIService
from app.utils.ai_utils import generate_ollama_response, OLLAMA_URL, OLLAMA_MODEL

chat_ns = Namespace('chat', description='Chatbot especializado LumiBot')

message_model = chat_ns.model('ChatMessage', {
    'mensaje': fields.String(required=True, description='Mensaje del usuario')
})

response_model = chat_ns.model('ChatResponse', {
    'respuesta': fields.String(description='Respuesta del chatbot')
})


PALABRAS_CLAVE = [
    'esp32',
    'bh1750',
    'sensor',
    'lux',
    'led',
    'pwm',
    'flask',
    'react',
    'docker',
    'mysql',
    'jwt',
    'dashboard',
    'salon',
    'salones',
    'actividad',
    'actividades',
    'consumo',
    'energia',
    'administrador',
    'alumno',
    'configuracion',
    'ollama',
    'iluminacion',
    'aws',
    'ec2',
    'api',
    'backend',
    'frontend'
]

ANALYSIS_KEYWORDS = {
    'analiza', 'analizar', 'analisis', 'estado', 'como', 'estuvo', 'reporte', 'diagnostico',
    'recomendacion', 'recomendaciones', 'consumo', 'lux', 'iluminacion', 'funcionando', 'funciona'
}
ROOM_KEYWORDS = {'salon', 'salones', 'laboratorio', 'laboratorios', 'aula', 'aulas', 'sala', 'salas'}
STOP_WORDS = {'el', 'la', 'los', 'las', 'del', 'de', 'al', 'para', 'y', 'o', 'como', 'esta', 'estuvo', 'analiza', 'analizar', 'analisis', 'estado', 'reporte', 'diagnostico', 'recomendacion', 'recomendaciones', 'consumo', 'lux', 'iluminacion', 'funcionando', 'funciona'}


def normalize_text(text):
    if not text:
        return ''

    normalized = unicodedata.normalize('NFKD', str(text))
    normalized = normalized.encode('ascii', 'ignore').decode('ascii')
    normalized = normalized.lower()
    normalized = ''.join(ch if ch.isalnum() or ch.isspace() else ' ' for ch in normalized)
    normalized = ' '.join(normalized.split())
    return normalized


NORMALIZED_PALABRAS_CLAVE = set(normalize_text(' '.join(PALABRAS_CLAVE)).split())


def detect_analysis_intent(text):
    normalized = normalize_text(text)
    if not normalized:
        return False

    tokens = normalized.split()
    has_room_context = any(token in ROOM_KEYWORDS for token in tokens)
    has_general_analysis_context = any(token in {'consumo', 'lux', 'iluminacion', 'estado', 'reporte', 'diagnostico', 'recomendacion', 'recomendaciones'} for token in tokens)
    has_analysis_context = any(token in ANALYSIS_KEYWORDS for token in tokens)

    if has_room_context:
        return has_analysis_context

    return has_general_analysis_context or (has_analysis_context and 'como' in tokens and len(tokens) >= 3)


def identify_salon(text):
    normalized = normalize_text(text)
    if not normalized:
        return None

    tokens = normalized.split()
    room_index = None

    for index, token in enumerate(tokens):
        if token in ROOM_KEYWORDS:
            room_index = index
            break

    if room_index is None:
        return None

    reference_tokens = []
    for token in tokens[room_index + 1:]:
        if token in STOP_WORDS:
            continue
        reference_tokens.append(token)
        if len(reference_tokens) >= 3:
            break

    if not reference_tokens:
        return None

    reference_phrase = ' '.join(reference_tokens)
    candidate_references = []
    if reference_phrase:
        candidate_references.append(reference_phrase)
    if room_index >= 0:
        candidate_references.append(tokens[room_index] + ' ' + reference_phrase if reference_phrase else tokens[room_index])

    for reference in candidate_references:
        if not reference:
            continue
        if reference.isdigit():
            salon = Salon.query.filter(Salon.id == int(reference)).first()
            if salon:
                return salon

        normalized_reference = normalize_text(reference)
        for salon in Salon.query.all():
            normalized_name = normalize_text(salon.nombre)
            if normalized_name == normalized_reference:
                return salon
            if normalized_reference in normalized_name.split():
                return salon
            if normalized_name in normalized_reference.split():
                return salon

    return None


@chat_ns.route('')
class Chat(Resource):

    @chat_ns.expect(message_model, validate=True)
    @chat_ns.response(200, 'Respuesta generada', response_model)
    @chat_ns.response(400, 'Solicitud inválida', response_model)

    def post(self):

        payload = request.get_json() or {}
        pregunta = str(payload.get("mensaje", "")).strip()

        if not pregunta:
            return {
                "respuesta": "Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica."
            }, 400

        pregunta_normalizada = normalize_text(pregunta)

        if detect_analysis_intent(pregunta):
            salon = identify_salon(pregunta)
            if salon is None:
                return {"respuesta": "No pude identificar el salón que deseas analizar. Por favor indica el nombre o número del salón."}, 200

            try:
                room_analysis = AIService.analyze_room(salon.id)
                respuesta = room_analysis.get('analisis') if isinstance(room_analysis, dict) else None
                if not respuesta:
                    respuesta = "No existen suficientes datos registrados para generar un análisis confiable."
                return {"respuesta": respuesta}, 200
            except requests.exceptions.Timeout:
                return {"respuesta": "LumiBot tardó demasiado en responder."}, 500
            except requests.exceptions.ConnectionError:
                return {"respuesta": "No fue posible conectar con Ollama."}, 500
            except Exception as e:
                import traceback
                traceback.print_exc()
                return {"respuesta": f"Error interno: {str(e)}"}, 500

        permitido = any(
            palabra in pregunta_normalizada
            for palabra in NORMALIZED_PALABRAS_CLAVE
        )

        print("=" * 60)
        print("Pregunta:", pregunta)
        print("=" * 60)

        if not permitido:
            return {
                "respuesta": "Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica."
            }, 200

        try:

            print("Enviando petición a Ollama...")
            print("URL:", OLLAMA_URL)
            print("Modelo:", OLLAMA_MODEL)

            respuesta = generate_ollama_response(pregunta)
            if not respuesta:
                respuesta = "Lo siento, no pude generar una respuesta."

            return {
                "respuesta": respuesta
            }, 200
        except Exception as e:

            import traceback
            traceback.print_exc()

            return {
                "respuesta": f"Error interno: {str(e)}"
            }, 500