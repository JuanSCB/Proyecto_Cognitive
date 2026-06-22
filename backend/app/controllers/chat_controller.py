from flask_restx import Namespace, Resource, fields
from flask import request
import requests

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
    'profesor',
    'alumno',
    'configuracion',
    'ollama',
    'iluminacion'
]

MISTRAL_PROMPT = '''
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

Si la pregunta está fuera del dominio permitido, responde exactamente:

"Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica."

Limita tus respuestas a un máximo de 5 líneas.
'''

@chat_ns.route('')
class Chat(Resource):
    @chat_ns.expect(message_model, validate=True)
    @chat_ns.response(200, 'Respuesta generada', response_model)
    @chat_ns.response(400, 'Solicitud inválida', response_model)
    def post(self):
        payload = request.get_json() or {}
        pregunta = str(payload.get('mensaje', '')).strip()

        if not pregunta:
            return {'respuesta': 'Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica.'}, 400

        pregunta_lower = pregunta.lower()
        permitido = any(palabra in pregunta_lower for palabra in PALABRAS_CLAVE)

        print("Pregunta:", pregunta)

        if not permitido:
            return {
                'respuesta': 'Lo siento, solo puedo responder preguntas relacionadas con el Sistema Inteligente de Iluminación Académica.'
            }, 200
        try:
            print("Enviando petición a Ollama")
            response = requests.post(
                'http://host.docker.internal:11434/api/generate',
                json={
                    'model': 'mistral',
                    'prompt': MISTRAL_PROMPT + '\n\nUsuario: ' + pregunta + '\nLumiBot:',
                    'stream': False
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            print(response.status_code)
            print(response.text)
            print(data)
            answer = data.get('response', '').strip()

            if not answer:
                answer = 'Lo siento, no pude generar una respuesta en este momento.'

            return {'respuesta': answer}
        except Exception as e:
            import traceback
            traceback.print_exc()

            return {
                'respuesta': f"{type(e).__name__}: {e}"
            }, 500
