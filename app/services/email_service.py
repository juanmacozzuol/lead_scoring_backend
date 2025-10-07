import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Template
from datetime import datetime
from app.models.email_models import EmailLog

# Cargar SendGrid API key desde .env
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@bdt.com")

# Lista simulada para registrar envíos (prototipo)
email_logs = []

# Generación de borrador
def generate_email_draft(client_name, age, segment, custom_text=None):
    # Elegimos estilo según perfil
    style = "formal" if age > 40 or segment == "corporate" else "informal"
    
    # Template HTML simple
    html_template = """
    <html>
      <body>
        <img src="https://BDT.com/logo.png" alt="Logo" width="150"/>
        <p>Hola {{ client_name }},</p>
        {% if style == 'formal' %}
        <p>Nos complace informarle acerca de nuestras últimas novedades.</p>
        {% else %}
        <p>¡Hola! Tenemos noticias geniales para vos.</p>
        {% endif %}
        {% if custom_text %}
        <p>{{ custom_text }}</p>
        {% endif %}
        <p>Saludos,<br/>El equipo de BDT</p>
      </body>
    </html>
    """
    template = Template(html_template)
    body_html = template.render(client_name=client_name, style=style, custom_text=custom_text)
    subject = "Noticias de BDT"

    return subject, body_html

# Envío de correo 
def send_email(to_email, subject, body_html):
    if not SENDGRID_API_KEY:
        raise RuntimeError("SENDGRID_API_KEY no configurada")

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body_html
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        # Registrar envío
        log = EmailLog(client_email=to_email, subject=subject, body_html=body_html,
                       status="sent", sent_at=datetime.utcnow())
        email_logs.append(log)
        return log
    except Exception as e:
        log = EmailLog(client_email=to_email, subject=subject, body_html=body_html,
                       status="failed", error_message=str(e))
        email_logs.append(log)
        raise e
