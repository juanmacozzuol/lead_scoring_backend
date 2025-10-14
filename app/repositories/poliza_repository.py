from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_estadisticas_polizas(db: Session, id_persona: int):
    """
    Retorna estadísticas agregadas de las pólizas de una persona.
    Incluye cantidad, suma asegurada total, costo total y prima promedio.
    """
    query = text("""
        SELECT 
            COUNT(*) AS cantidad_polizas,
            COALESCE(SUM(prima_pagada), 0) AS costo_mensual_total_seguro,
            COALESCE(SUM(suma_asegurada), 0) AS suma_asegurada_total,
            COALESCE(AVG(prima_pagada), 0) AS prima_promedio
        FROM polizas
        WHERE id_persona = :id_persona
    """)
    return db.execute(query, {"id_persona": id_persona}).fetchone()
