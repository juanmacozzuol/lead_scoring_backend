from sqlalchemy.orm import Session
from typing import List
from app.database.models import Correo

def obtener_historial_por_persona(db: Session, id_persona: int) -> List[Correo]:
    """
    Busca todos los correos enviados a una persona especifica (historial).
    Ordena por fecha de creacion (mas nuevo primero).
    """
    
    return db.query(Correo).filter(
        Correo.id_persona == id_persona
    ).order_by(
        Correo.fecha_creacion.desc() # Ordena por la fecha de creacion
    ).all()