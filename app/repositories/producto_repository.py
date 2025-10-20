from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_tipos_productos_por_persona(db: Session, id_persona: int):
    """
    Devuelve una lista con los tipos de productos (seguros)
    asociados a las pólizas de una persona.
    """
    result = db.execute(
        text("""
            SELECT LOWER(tipo_seguro) AS tipo
            FROM polizas
            WHERE id_persona = :id_persona
        """),
        {"id_persona": id_persona}
    ).scalars().all()
    return result or []
