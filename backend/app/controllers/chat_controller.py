from flask_restx import Namespace, Resource, fields
from flask import request
import requests
import os

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
    'profesor',
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
- Roles Profesor y Alumno
- Arquitectura del sistema
- Comunicación ESP32 ↔ Flask ↔ MySQL ↔ React

Responde de forma técnica, clara y breve.

No inventes información.

No respondas preguntas sobre deportes, política, historia, matemáticas, cultura general, entretenimiento o cualquier tema ajeno al proyecto.

Si la pregunta está fuera del dominio permitido responde exactamente:

Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica.

Limita las respuestas a máximo cinco líneas.
"""


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

        pregunta_lower = pregunta.lower()

        permitido = any(
            palabra in pregunta_lower
            for palabra in PALABRAS_CLAVE
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