from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_estadisticas_siniestros(db: Session, id_persona: int):
    """
    Retorna cantidad, monto promedio y días desde el último siniestro.
    """
    query = text("""
        SELECT 
            COUNT(s.id_siniestro) AS cantidad_siniestros,
            COALESCE(AVG(s.monto_reclamado), 0) AS monto_promedio_siniestro,
            COALESCE(DATEDIFF(CURDATE(), MAX(s.fecha_reporte)), 999) AS dias_desde_ultimo_siniestro
        FROM siniestros s
        JOIN polizas p ON s.id_poliza = p.id_poliza
        WHERE p.id_persona = :id_persona
    """)
    return db.execute(query, {"id_persona": id_persona}).fetchone()
