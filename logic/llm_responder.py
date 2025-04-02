import os
import requests
from dotenv import load_dotenv

# Cargar token desde archivo .env
load_dotenv()
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def responder_llm(pregunta):
    """
    Envía una pregunta al modelo de Hugging Face y retorna la respuesta generada.
    """
    if not API_TOKEN:
        raise EnvironmentError("No se encontró el token de Hugging Face en el entorno.")

    payload = {
        "inputs": f"[INST] {pregunta} [/INST]"
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        else:
            return output
    else:
        raise RuntimeError(f"Error al llamar al modelo: {response.status_code} - {response.text}")
