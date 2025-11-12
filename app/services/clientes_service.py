from app.repositories.persona_repository import get_all_clients

def get_all_clients_service(db):
    """
    Lógica de negocio para obtener todos los clientes.
    """
    try:
        clients = get_all_clients(db)
        return clients
    except Exception as e:
        import traceback
        print("❌ Error al obtener clientes:")
        traceback.print_exc()
        return {"error": f"No se pudieron obtener los clientes: {str(e)}"}
