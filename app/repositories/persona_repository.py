from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_persona_por_dni(db: Session, dni: str):
    """
    Obtiene una persona de la base de datos por su DNI.
    Retorna el objeto Row o None si no existe.
    """
    query = text("SELECT * FROM personas WHERE dni = :dni")
    return db.execute(query, {"dni": dni}).fetchone()


def obtener_provincia_por_persona(db: Session, id_persona: int):
    """
    Devuelve la provincia asociada a una persona, si tiene dirección cargada.
    """
    query = text("""
        SELECT provincia FROM direccion 
        WHERE id_persona = :id_persona
        LIMIT 1
    """)
    return db.execute(query, {"id_persona": id_persona}).scalar()
