import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables desde .env
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
for model in genai.list_models():
    print(model)
