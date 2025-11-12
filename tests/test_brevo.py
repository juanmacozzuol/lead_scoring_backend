import os
from pprint import pprint
from dotenv import load_dotenv
import brevo_python
from brevo_python.models.send_smtp_email import SendSmtpEmail

# Cargar variables desde .env
load_dotenv()

# Configuracion
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@BDT.com")
TO_EMAIL = os.getenv("TO_EMAIL", "ejemplo@ejemplo.com")  # Cambiar por el email de prueba
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

if not BREVO_API_KEY:
    raise ValueError("No se encontró BREVO_API_KEY en .env")

# Configuracion del cliente
configuracion = brevo_python.Configuration()
configuracion.api_key['api-key'] = BREVO_API_KEY
api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuracion))

# Preparar email de prueba
send_email = SendSmtpEmail(
    to=[{"email": TO_EMAIL}],
    html_content="<p>¡Hola! Este es un test desde Brevo.</p>",
    subject="Prueba de Brevo SDK",
    sender={"email": FROM_EMAIL, "name": "BDT Seguros"}
)

# Enviar
try:
    response = api_instance.send_transac_email(send_email)
    print("Correo enviado con éxito.")
    pprint(response.to_dict())
except Exception as e:
    print("Error al enviar correo:", e)
