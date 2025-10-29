import os
from dotenv import load_dotenv
import re
import json
import pytest
import google.generativeai as genai
import openai

from app.services import llm_service

# Cargar variables de .env
load_dotenv()

# Detectar proveedor disponible
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if GOOGLE_API_KEY:
    PROVIDER = "google"
    genai.configure(api_key=GOOGLE_API_KEY)
elif OPENAI_API_KEY:
    PROVIDER = "openai"
    openai.api_key = OPENAI_API_KEY
else:
    PROVIDER = None

@pytest.mark.integration
def test_generar_json_email_real():
    if PROVIDER is None:
        pytest.skip("No se encontró GOOGLE_API_KEY ni OPENAI_API_KEY, se saltea el test de integración")

    prompt = """
        Eres un asistente de ventas experto de la compañía "BDT Seguros".
        Redacta un email de prueba en HTML básico con asunto y cuerpo.
        Devuelve un JSON con EXACTAMENTE estas claves:
        {
            "asunto_sugerido": "Texto del asunto",
            "cuerpo_sugerido": "Texto del email en HTML"
        }
        No incluyas nada más fuera del JSON.
    """

    # Llamada real al LLM según proveedor
    try:
        response_text = llm_service.generar_json_email(prompt)
    except Exception as e:
        pytest.fail(f"Error al llamar al LLM ({PROVIDER}): {e}")

    # Extraer JSON si hay texto extra
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    assert json_match, f"Respuesta no contiene JSON: {response_text}"

    # Parsear
    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        pytest.fail(f"Respuesta no es JSON válido: {response_text}")

    # Validar claves
    assert "asunto_sugerido" in data, "Falta la clave 'asunto_sugerido'"
    assert "cuerpo_sugerido" in data, "Falta la clave 'cuerpo_sugerido'"

    # Validar HTML básico en cuerpo
    assert "<p>" in data["cuerpo_sugerido"] or "<br>" in data["cuerpo_sugerido"], \
        "El cuerpo del email no contiene HTML básico (<p> o <br>)"

    print(f"Respuesta generada por el LLM ({PROVIDER}):")
    print(json.dumps(data, indent=2))
