from fastapi import HTTPException
from datetime import date
from sqlalchemy import text

from app.repositories.persona_repository import (
    obtener_persona_por_dni,
    obtener_provincia_por_persona,
)
from app.repositories.poliza_repository import obtener_estadisticas_polizas
from app.repositories.siniestro_repository import obtener_estadisticas_siniestros
from app.repositories.producto_repository import obtener_tipos_productos_por_persona
from app.repositories.pago_repository import obtener_cantidad_cuotas_impagas_por_persona
from app.services.predict_service import predecir_cross_selling
from app.models.insurance_db_models import ScoreEvent


# -------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def calcular_antiguedad(fecha_registro):
    if not fecha_registro:
        return 0
    hoy = date.today()
    return (hoy.year - fecha_registro.year) * 12 + (hoy.month - fecha_registro.month)


# -------------------------------------------------------
# ENDPOINT PRINCIPAL /predict/{dni}
# -------------------------------------------------------

def obtener_prediccion_por_dni(dni: str, db):
    try:
        # 1) Buscar persona
        persona = obtener_persona_por_dni(db, dni)
        if not persona:
            raise HTTPException(status_code=404, detail="No se encontró ninguna persona con ese DNI")

        # 2) Construcción de features
        edad = calcular_edad(persona.fecha_nacimiento)
        antiguedad = calcular_antiguedad(persona.fecha_registro)
        provincia = obtener_provincia_por_persona(db, persona.id_persona) or "buenos aires"

        poliza_data = obtener_estadisticas_polizas(db, persona.id_persona)
        siniestro_data = obtener_estadisticas_siniestros(db, persona.id_persona)
        productos_activos = obtener_tipos_productos_por_persona(db, persona.id_persona)
        cuotas_impagas = obtener_cantidad_cuotas_impagas_por_persona(db, persona.id_persona)

        features = {
            "edad": int(edad),
            "genero": str(persona.genero or "no especificado").lower(),
            "hijos": int(persona.cantidad_hijos or 0),
            "vivienda_propia": int(persona.vivienda_propia),
            "posee_auto": int(persona.posee_auto),

            "tiene_auto": int("auto" in productos_activos),
            "tiene_hogar": int("hogar" in productos_activos),
            "tiene_vida": int("vida" in productos_activos),
            "tiene_salud": int("salud" in productos_activos),

            "antiguedad_cliente": int(antiguedad),
            "cuotas_impagas": int(cuotas_impagas),

            "cantidad_polizas": int(poliza_data.cantidad_polizas if poliza_data else 0),
            "costo_mensual_total_seguro": float(poliza_data.costo_mensual_total_seguro if poliza_data else 0),
            "suma_asegurada_total": float(poliza_data.suma_asegurada_total if poliza_data else 0),
            "prima_promedio": float(poliza_data.prima_promedio if poliza_data else 0),

            "cantidad_siniestros": int(siniestro_data.cantidad_siniestros if siniestro_data else 0),
            "monto_promedio_siniestro": float(siniestro_data.monto_promedio_siniestro if siniestro_data else 0),
            "dias_desde_ultimo_siniestro": int(siniestro_data.dias_desde_ultimo_siniestro if siniestro_data else 999),

            "ocupacion": str(persona.ocupacion or "no especificado").lower(),
            "estado_civil": str(persona.estado_civil or "soltero").lower(),
            "provincia": str(provincia).lower(),

            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "nombre_completo": f"{persona.nombre} {persona.apellido}",
        }

        # 3) Traer polizas para el modal
        query_polizas = """
            SELECT tipo_seguro, cobertura, suma_asegurada, prima_pagada, estado
            FROM polizas
            WHERE id_persona = :id_persona AND estado = 'Activa'
        """
        polizas = db.execute(text(query_polizas), {"id_persona": persona.id_persona}).fetchall()
        features["polizas_detalle"] = [dict(row._mapping) for row in polizas]

        
        score_existente = (
            db.query(ScoreEvent)
            .filter(ScoreEvent.id_persona == persona.id_persona)
            .first()
        )

        if score_existente:
         
           
            resultado = predecir_cross_selling(features)

            return {
                "dni": dni,
                "nombre": persona.nombre,
                "apellido": persona.apellido,
                "score": score_existente.puntaje,
                "nivel": score_existente.nivel_score,
                "productos_recomendados": resultado["productos_recomendados"],
                "features": features,
            }

       
        print(" Calculando score ")
        resultado = predecir_cross_selling(features)

        nuevo = ScoreEvent(
            puntaje=resultado["score"],
            nivel_score=resultado["nivel"],
            fecha_creacion=date.today(),
            id_persona=persona.id_persona
        )
        db.add(nuevo)
        db.commit()

        return {
            "dni": dni,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "score": resultado["score"],
            "nivel": resultado["nivel"],
            "productos_recomendados": resultado["productos_recomendados"],
            "features": features,
        }

    except Exception as e:
        print("❌ Error general:", e)
        raise HTTPException(status_code=500, detail=str(e))
