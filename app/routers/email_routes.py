from fastapi import APIRouter
# Import the required models for type hinting the response and request
from app.models.email_models import DraftEmailRequest, DraftEmailResponse, SendEmailRequest, SendEmailResponse
# Import the logic handlers (controllers)
from app.controllers.email_controller import get_email_draft_logic, send_email_endpoint_logic, get_email_history_logic

# El 'router' es la instancia que contiene todas tus rutas.
# SE ELIMINA EL PREFIJO "/email" porque ya se lo aplica el router general.
router = APIRouter(
    tags=["Email Operations"]
)

# Endpoint para generar borrador. La ruta final será /email/draft.
@router.post(
    "/draft", 
    response_model=DraftEmailResponse, 
    summary="Generate Email Draft"
)
def get_email_draft(req: DraftEmailRequest):
    """
    Generates a personalized email draft (subject and body) based on client data.
    """
    # Logic is delegated entirely to the controller
    return get_email_draft_logic(req)

# Endpoint para enviar correo. La ruta final será /email/send.
@router.post(
    "/send", 
    response_model=SendEmailResponse, 
    summary="Send Email"
)
def send_email_endpoint(req: SendEmailRequest):
    """
    Sends the compiled email and logs the attempt.
    """
    # Logic is delegated entirely to the controller
    return send_email_endpoint_logic(req)

# Endpoint opcional para historial. La ruta final será /email/history.
@router.get(
    "/history", 
    response_model=list[SendEmailResponse],
    summary="Get Email History"
)
def get_email_history():
    """
    Retrieves the history of emails sent.
    """
    # Logic is delegated entirely to the controller
    return get_email_history_logic()