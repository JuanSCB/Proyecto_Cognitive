from flask_restx import Namespace, Resource, fields
from flask import request
import requests
import os
import unicodedata
from app import db
from app.models.salon import Salon
from app.models.sensor import Sensor
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico
from app.models.activity import Actividad
from app.models.configuracion import Configuracion

chat_ns = Namespace('chat', description='Chatbot especializado LumiBot')

message_model = chat_ns.model('ChatMessage', {
    'mensaje': fields.String(required=True, description='Mensaje del usuario')
})

response_model = chat_ns.model('ChatResponse', {
    'respuesta': fields.String(description='Respuesta del chatbot')
})

# URL de Ollama obtenida desde Docker Compose
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

# Modelo a utilizar
OLLAMA_MODEL = "gemma3:1b"
# Si más adelante utilizas Mistral, simplemente cambia por:
# OLLAMA_MODEL = "mistral"

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

SYSTEM_PROMPT = """
Eres LumiBot.

Asistente virtual del proyecto
"Sistema Inteligente de Iluminación Académica".

Tu conocimiento se limita exclusivamente a:

- ESP32 DevKit V1
- Sensor BH1750
- Lux
- PWM
- Flask
- React
- Docker
- AWS EC2
- MySQL
- JWT
- Ollama
- Dashboard de monitoreo
- Salones
- Actividades académicas
- Consumo energético
- Roles Administrador y Alumno
- Arquitectura del sistema
- Comunicación ESP32 ↔ Flask ↔ MySQL ↔ React

Responde de forma técnica, clara y breve.

No inventes información.

No respondas preguntas sobre deportes, política, historia, matemáticas, cultura general, entretenimiento o cualquier tema ajeno al proyecto.

Si la pregunta está fuera del dominio permitido responde exactamente:

Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica.

Limita las respuestas a máximo cinco líneas.
"""

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


def _build_room_analysis_prompt(salon):
    latest_sensor = (
        Sensor.query.filter_by(salon_id=salon.id)
        .order_by(Sensor.registrado_en.desc())
        .first()
    )

    history_entries = (
        db.session.query(HistorialIluminacion)
        .join(Sensor)
        .filter(Sensor.salon_id == salon.id)
        .order_by(HistorialIluminacion.registrado_en.desc())
        .limit(5)
        .all()
    )

    consumo_entry = (
        db.session.query(ConsumoEnergetico)
        .join(Sensor)
        .filter(Sensor.salon_id == salon.id)
        .order_by(ConsumoEnergetico.creado_en.desc())
        .first()
    )

    configuracion = Configuracion.query.order_by(Configuracion.creado_en.desc()).first()
    actividad_actual = salon.actividad.nombre if salon.actividad else None

    lux_actual = latest_sensor.lux if latest_sensor else None
    lux_promedio = round(sum(item.lux for item in history_entries) / len(history_entries), 2) if history_entries else None
    intensidad = latest_sensor.intensidad_led if latest_sensor else None
    consumo = consumo_entry.total_kwh if consumo_entry else (latest_sensor.consumo_energetico if latest_sensor else None)
    modo = 'automático' if latest_sensor and latest_sensor.modo_automatico else 'manual' if latest_sensor else 'No disponible'
    fecha = latest_sensor.registrado_en.strftime('%Y-%m-%d %H:%M:%S') if latest_sensor and latest_sensor.registrado_en else None

    if not history_entries and not latest_sensor:
        return None

    prompt = (
        "Eres un ingeniero especialista en automatización industrial y eficiencia energética.\n"
        "Analiza el siguiente salón del sistema LumiSense.\n\n"
        f"Nombre del salón: {salon.nombre or 'No disponible'}\n"
        f"Actividad: {actividad_actual or 'No disponible'}\n"
        f"Modo: {modo}\n"
        f"Lux actual: {lux_actual if lux_actual is not None else 'No disponible'}\n"
        f"Lux promedio: {lux_promedio if lux_promedio is not None else 'No disponible'}\n"
        f"Consumo energético: {consumo if consumo is not None else 'No disponible'}\n"
        f"PWM LED: {intensidad if intensidad is not None else 'No disponible'}\n"
        f"Fecha: {fecha or 'No disponible'}\n"
        f"Configuración recomendada: {configuracion.umbral_lux if configuracion else 'No disponible'}\n\n"
        "Genera:\n"
        "1. Estado general del salón.\n"
        "2. Diagnóstico técnico.\n"
        "3. Posibles problemas.\n"
        "4. Recomendaciones para optimizar iluminación y consumo energético.\n"
        "5. Conclusión.\n"
        "No inventes información.\n"
        "Si los datos no permiten llegar a una conclusión indícalo.\n"
        "Responder siempre en español.\n"
        "Máximo seis líneas."
    )

    return prompt

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
        pregunta_lower = pregunta.lower()

        if detect_analysis_intent(pregunta):
            salon = identify_salon(pregunta)
            if salon is None:
                return {"respuesta": "No pude identificar el salón que deseas analizar. Por favor indica el nombre o número del salón."}, 200

            prompt = _build_room_analysis_prompt(salon)
            if not prompt:
                return {"respuesta": "No existen suficientes datos registrados para generar un análisis confiable."}, 200

            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={
                        "model": OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "system": "Eres un ingeniero experto en automatización, eficiencia energética, IoT y sistemas inteligentes de iluminación."
                    },
                    timeout=120
                )
                response.raise_for_status()
                data = response.json()
                respuesta = data.get("response", "").strip()
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

            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": f"{SYSTEM_PROMPT}\n\nUsuario: {pregunta}\nLumiBot:",
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            respuesta = data.get("response", "").strip()

            if not respuesta:
                respuesta = "Lo siento, no pude generar una respuesta."

            print("Respuesta generada correctamente.")

            return {
                "respuesta": respuesta
            }, 200

        except requests.exceptions.Timeout:
            return {
                "respuesta": "LumiBot tardó demasiado en responder."
            }, 500

        except requests.exceptions.ConnectionError:
            return {
                "respuesta": "No fue posible conectar con Ollama."
            }, 500

        except Exception as e:

            import traceback
            traceback.print_exc()

            return {
                "respuesta": f"Error interno: {str(e)}"
            }, 500