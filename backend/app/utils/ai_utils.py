import os
import re
import requests

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')
OLLAMA_MODEL = 'gemma3:1b'
AI_SYSTEM_INSTRUCTION = (
    'Eres un ingeniero experto en eficiencia energética, automatización y sistemas inteligentes de iluminación. '
    'Responde sin formato Markdown, sin viñetas ni títulos, solo texto plano. '
    'Si la información disponible no es suficiente para responder con certeza, indícalo explícitamente y no inventes datos.'
)


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
