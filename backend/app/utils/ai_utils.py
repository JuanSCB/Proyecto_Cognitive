import os
import re
import requests

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')
OLLAMA_MODEL = 'gemma3:1b'
AI_SYSTEM_INSTRUCTION = (
    'Eres un ingeniero especialista en iluminación inteligente y eficiencia energética. '
    'Analiza únicamente la información proporcionada por el backend. '
    'No inventes porcentajes de ahorro, eficiencias, consumos, diagnósticos, cálculos, comparaciones ni recomendaciones si no están respaldados por los datos. '
    'Si algún dato no está disponible, indícalo claramente. '
    'Lux menores a 100 indican iluminación insuficiente. '
    'Entre 100 y 6000 lux se considera una iluminación adecuada para el funcionamiento del sistema. '
    'Mayores a 6000 lux indican abundante iluminación natural y normalmente no es necesario utilizar iluminación artificial. '
    'El consumo energético mostrado por el sistema es un valor estimado. '
    'El control de iluminación es realizado por un ESP32 utilizando un sensor BH1750 y un foco halógeno regulado mediante PWM. '
    'La respuesta debe ser profesional, técnica, concisa y en español. '
    'No utilices Markdown, negritas, viñetas, emojis, caracteres especiales, encabezados ni listas numeradas. '
    'La respuesta debe tener entre 6 y 10 líneas. '
    'Si la información es insuficiente, indícalo explícitamente y explica qué datos adicionales serían necesarios. '
    'Nunca inventes información para completar una respuesta.'
)


def build_lumibot_analysis_prompt(salon, latest_sensor, history_entries, consumo_entry):
    actividad_actual = salon.actividad.nombre if salon.actividad else None
    lux_actual = latest_sensor.lux if latest_sensor else None
    lux_promedio = round(sum(item.lux for item in history_entries) / len(history_entries), 2) if history_entries else None
    intensidad_led = latest_sensor.intensidad_led if latest_sensor else None
    consumo_energetico = consumo_entry.total_kwh if consumo_entry else (latest_sensor.consumo_energetico if latest_sensor else None)
    modo = 'automático' if latest_sensor and latest_sensor.modo_automatico else 'manual' if latest_sensor else 'No disponible'
    fecha = latest_sensor.registrado_en.strftime('%Y-%m-%d %H:%M:%S') if latest_sensor and latest_sensor.registrado_en else 'No disponible'

    prompt = (
        'Datos del salón\n'
        f'Nombre: {salon.nombre or "No disponible"}\n'
        f'Actividad: {actividad_actual or "No disponible"}\n'
        f'Modo de funcionamiento: {modo}\n'
        f'Iluminancia actual: {lux_actual if lux_actual is not None else "No disponible"}\n'
        f'Iluminancia promedio: {lux_promedio if lux_promedio is not None else "No disponible"}\n'
        f'Intensidad LED (%): {intensidad_led if intensidad_led is not None else "No disponible"}\n'
        f'Consumo energético estimado: {consumo_energetico if consumo_energetico is not None else "No disponible"}\n'
        f'Fecha de la medición: {fecha}\n\n'
        'Analiza estos datos con las reglas del sistema. '
        'Responde siguiendo exactamente la estructura: Estado general, Evaluación técnica, Observaciones, Recomendaciones. '
        'Si la información es insuficiente, indícalo explícitamente y explica qué datos adicionales serían necesarios.'
    )

    return prompt


def clean_ollama_text(text):
    if text is None:
        return ''
    text = str(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'(^|\n)[ \t]*[#*]+[ \t]*', r'\1', text)
    text = re.sub(r'[\*#]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def generate_ollama_response(prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False,
            'system': AI_SYSTEM_INSTRUCTION
        },
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, dict):
        data = {}

    return clean_ollama_text(data.get('response', ''))
