from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.clientes_controller import get_all_clients_controller

router = APIRouter( tags=["Clientes"])

@router.get("/")
def get_all_clients_route(db: Session = Depends(get_db)):
    """
    Endpoint que devuelve todos los clientes de la base de datos.
    """
    return get_all_clients_controller(db)
