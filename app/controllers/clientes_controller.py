from app.services.clientes_service import get_all_clients_service

def get_all_clients_controller(db):
    """
    Controlador que obtiene todos los clientes desde el service.
    """
    return get_all_clients_service(db)
