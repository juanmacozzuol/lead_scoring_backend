from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_cantidad_cuotas_impagas_por_persona(db: Session, id_persona: int):
    """
    Devuelve la cantidad total de cuotas impagas
    asociadas a todas las pólizas de una persona.
    """
    result = db.execute(
        text("""
            SELECT COUNT(*) 
            FROM pagos p
            JOIN polizas po ON p.id_poliza = po.id_poliza
            WHERE po.id_persona = :id_persona
              AND LOWER(p.estado_pago) = 'impago'
        """),
        {"id_persona": id_persona}
    ).scalar()
    return result or 0
