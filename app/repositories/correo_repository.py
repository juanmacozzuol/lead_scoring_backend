from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from typing import List
from app.models.email_db_models import Correo
from app.models.user_db_models import Persona, Usuario

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

def obtener_todos_los_correos(db: Session) -> List:
    """
    Devuelve todos los correos con el email de la persona y el nombre del usuario.
    """
    resultados = (
        db.query(Correo, Persona.email, Usuario.nombre_usuario)
        .join(Persona, Correo.id_persona == Persona.id_persona)
        .join(Usuario, Correo.id_usuario == Usuario.id_usuario)
        .order_by(Correo.fecha_creacion.desc())
        .all()
    )
    return resultados