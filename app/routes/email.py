from fastapi import APIRouter, HTTPException
from app.models.email_models import DraftEmailRequest, DraftEmailResponse, SendEmailRequest, SendEmailResponse
from app.services.email_service import generate_email_draft, send_email, email_logs

router = APIRouter()

# Endpoint para generar borrador 
@router.post("/draft", response_model=DraftEmailResponse)
def get_email_draft(req: DraftEmailRequest):
    try:
        subject, body_html = generate_email_draft(req.client_name, req.age, req.segment, req.custom_text)
        return DraftEmailResponse(subject=subject, body_html=body_html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para enviar correo 
@router.post("/send", response_model=SendEmailResponse)
def send_email_endpoint(req: SendEmailRequest):
    try:
        log = send_email(req.to_email, req.subject, req.body_html)
        return SendEmailResponse(status=log.status, message=f"Email enviado a {req.to_email}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint opcional para historial
@router.get("/history", response_model=list[SendEmailResponse])
def get_email_history():
    return [SendEmailResponse(status=log.status, message=f"Email a {log.client_email}") for log in email_logs]
