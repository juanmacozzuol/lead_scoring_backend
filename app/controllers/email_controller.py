from fastapi import HTTPException
from app.models.email_models import DraftEmailRequest, DraftEmailResponse, SendEmailRequest, SendEmailResponse
from app.services.email_service import generate_email_draft, send_email, email_logs

# --- Controller Functions ---

def get_email_draft_logic(req: DraftEmailRequest) -> DraftEmailResponse:
    """
    Handles the logic for generating a draft email based on client data.
    """
    try:
        # Call the service layer to perform the core task
        subject, body_html = generate_email_draft(req.client_name, req.age, req.segment, req.custom_text)
        
        # Return the response model instance
        return DraftEmailResponse(subject=subject, body_html=body_html)
    except Exception as e:
        # Raise an HTTPException if the service fails
        print(f"Error generating email draft: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar borrador: {str(e)}")


def send_email_endpoint_logic(req: SendEmailRequest) -> SendEmailResponse:
    """
    Handles the logic for sending a completed email.
    """
    try:
        # Call the service layer to perform the core task
        log = send_email(req.to_email, req.subject, req.body_html)
        
        # Return the response model instance
        return SendEmailResponse(status=log.status, message=f"Email enviado a {req.to_email}")
    except Exception as e:
        # Raise an HTTPException if the service fails
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Error al enviar correo: {str(e)}")


def get_email_history_logic() -> list[SendEmailResponse]:
    """
    Handles the logic for retrieving the email history.
    """
    # Map the internal log objects from email_service to the external SendEmailResponse model
    return [
        SendEmailResponse(status=log.status, message=f"Email a {log.client_email}") 
        for log in email_logs
    ]
