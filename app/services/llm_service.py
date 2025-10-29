import os
import httpx
import google.generativeai as genai
from openai import OpenAI
import json
from fastapi import HTTPException, status

# Lee la configuracion del .env
PROVIDER = os.getenv("LLM_PROVIDER", "google") # 'google', 'openai', o 'local'
LOCAL_URL = os.getenv("LOCAL_LLM_URL") # ej: "http://localhost:11434/api/generate"
LOCAL_MODEL = os.getenv("LOCAL_LLM_MODEL_NAME") # ej: "llama3"

# Cliente de OpenAI (se configura una vez)
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Advertencia: No se pudo configurar OpenAI (API Key?): {e}")
    openai_client = None

# Cliente de Google (se configura una vez)
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    google_model = genai.GenerativeModel("models/gemini-2.5-flash")
except Exception as e:
    print(f"Advertencia: No se pudo configurar Google AI (API Key?): {e}")
    google_model = None


def _call_google_ai(prompt: str) -> str:
    """Llama a la API de Google Gemini."""
    if not google_model:
        raise HTTPException(status_code=503, detail="Servicio de Google AI no configurado (falta API Key?)")
    try:
        response = google_model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a Google AI: {str(e)}")

def _call_openai(prompt: str) -> str:
    """Llama a la API de OpenAI (GPT)."""
    if not openai_client:
        raise HTTPException(status_code=503, detail="Servicio de OpenAI no configurado (falta API Key?)")
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o", # O el modelo que prefieras
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} # Pedimos JSON
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a OpenAI: {str(e)}")

def _call_local_llm(prompt: str) -> str:
    """Llama a un LLM local (ej. Ollama)."""
    if not LOCAL_URL or not LOCAL_MODEL:
        raise HTTPException(status_code=503, detail="LLM Local no configurado (LOCAL_LLM_URL y LOCAL_LLM_MODEL_NAME en .env)")
    
    # Formato de payload para Ollama
    payload = {
        "model": LOCAL_MODEL,
        "prompt": prompt,
        "format": "json", # Le pedimos a Ollama que fuerce la salida a JSON
        "stream": False
    }
    
    try:
        # Cliente sincrono con un timeout de 180s.
        with httpx.Client(timeout=180.0) as client:
            response = client.post(LOCAL_URL, json=payload)
            response.raise_for_status() # Lanza error si no es 200
            
            # Ollama devuelve el JSON dentro de un JSON, en la clave "response"
            # Parseamos el string de la respuesta para devolver solo el JSON del email
            respuesta_ollama = response.json()

            raw = respuesta_ollama.get("response", "")
            # En caso de que devuelva texto sin JSON (por modelo incompatible)
            if not raw.strip().startswith("{"):
                print("Advertencia: la respuesta no parece JSON. Se devolverá texto plano.")
            return raw
            
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error conectando al LLM local en {LOCAL_URL}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la respuesta del LLM local: {str(e)}")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="No se pudo conectar con Ollama. Revisar si esta activo en localhost:11434")



def generar_json_email(prompt: str) -> str:
    """
    Funcion publica unificada.
    Decide a que motor llamar segun el .env.
    Devuelve un string que DEBE ser un JSON valido.
    """
    
    print(f"Generando email con el proveedor: {PROVIDER}")
    
    if PROVIDER == "google":
        return _call_google_ai(prompt)
    elif PROVIDER == "openai":
        return _call_openai(prompt)
    elif PROVIDER == "local":
        return _call_local_llm(prompt)
    else:
        raise HTTPException(
            status_code=501, 
            detail=f"Proveedor LLM '{PROVIDER}' no es valido. Usar 'google', 'openai', o 'local'."
        )