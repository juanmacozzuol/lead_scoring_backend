from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Solicitud para generar borrador
class DraftEmailRequest(BaseModel):
    client_name: str
    client_email: EmailStr
    age: int
    segment: str
    custom_text: Optional[str] = None

# Respuesta con borrador
class DraftEmailResponse(BaseModel):
    subject: str
    body_html: str

# Solicitud para enviar correo
class SendEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body_html: str

# Respuesta envío
class SendEmailResponse(BaseModel):
    status: str
    message: str

# Registro de email enviado
class EmailLog(BaseModel):
    client_email: EmailStr
    subject: str
    body_html: str
    status: str
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
