from fastapi import HTTPException
from datetime import date
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
# Funciones auxiliares
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
# Controlador principal del endpoint /predict/{dni}
# -------------------------------------------------------

def obtener_prediccion_por_dni(dni: str, db):
    try:
        # 1️⃣ Busco la persona en la base de datos
        persona = obtener_persona_por_dni(db, dni)
        if not persona:
            raise HTTPException(status_code=404, detail="No se encontró ninguna persona con ese DNI")

        # 2️⃣ Calculo edad, antigüedad y provincia
        edad = calcular_edad(persona.fecha_nacimiento)
        antiguedad = calcular_antiguedad(persona.fecha_registro)
        provincia = obtener_provincia_por_persona(db, persona.id_persona) or "buenos aires"

        # 3️⃣ Traigo información de las tablas relacionadas
        poliza_data = obtener_estadisticas_polizas(db, persona.id_persona)
        siniestro_data = obtener_estadisticas_siniestros(db, persona.id_persona)
        productos = obtener_tipos_productos_por_persona(db, persona.id_persona)
        cuotas_impagas = obtener_cantidad_cuotas_impagas_por_persona(db, persona.id_persona)

        # 4️⃣ Mapeo de productos (para saber qué tiene activo)
        tiene_auto = int("auto" in productos)
        tiene_hogar = int("hogar" in productos)
        tiene_vida = int("vida" in productos)
        tiene_salud = int("salud" in productos)

        # 5️⃣ Armo las features que usará el modelo
        features = {
            "edad": edad,
            "genero": persona.genero.lower() if persona.genero else "no especificado",
            "hijos": persona.cantidad_hijos or 0,
            "vivienda_propia": int(persona.vivienda_propia),
            "posee_auto": int(persona.posee_auto),
            "tiene_auto": tiene_auto,
            "tiene_hogar": tiene_hogar,
            "tiene_vida": tiene_vida,
            "tiene_salud": tiene_salud,
            "antiguedad_cliente": antiguedad,
            "cuotas_impagas": cuotas_impagas,
            "cantidad_polizas": poliza_data.cantidad_polizas if poliza_data else 0,
            "costo_mensual_total_seguro": poliza_data.costo_mensual_total_seguro if poliza_data else 0,
            "suma_asegurada_total": poliza_data.suma_asegurada_total if poliza_data else 0,
            "prima_promedio": poliza_data.prima_promedio if poliza_data else 0,
            "cantidad_siniestros": siniestro_data.cantidad_siniestros if siniestro_data else 0,
            "monto_promedio_siniestro": siniestro_data.monto_promedio_siniestro if siniestro_data else 0,
            "dias_desde_ultimo_siniestro": siniestro_data.dias_desde_ultimo_siniestro if siniestro_data else 999,
            "ocupacion": persona.ocupacion.lower() if persona.ocupacion else "no especificado",
            "estado_civil": persona.estado_civil.lower() if persona.estado_civil else "soltero",
            "provincia": provincia.lower(),
        }

        # 🟣 Agregamos id, nombre, apellido y nombre completo
        features["id"] = persona.id_persona
        features["nombre"] = persona.nombre
        features["apellido"] = persona.apellido if hasattr(persona, "apellido") else ""
        features["nombre_completo"] = f"{persona.nombre} {persona.apellido}".strip()
        features["email"] = persona.email
        # 6️⃣ Llamo al servicio que ejecuta el modelo
        resultado = predecir_cross_selling(features)

        # 7️⃣ Guardo el resultado en la tabla de ScoreEvent
        try:
            nuevo_score = ScoreEvent(
                puntaje=resultado["score"],
                nivel_score=resultado["nivel"],
                fecha_creacion=date.today(),
                id_persona=persona.id_persona
            )
            db.add(nuevo_score)
            db.commit()
            print(f"✅ Score registrado para persona id {persona.id_persona}")
        except Exception as e:
            db.rollback()
            print(f"⚠️ Error al guardar el score en la base de datos: {e}")

        # 8️⃣ Consulto el último score registrado
        ultimo_score = (
            db.query(ScoreEvent)
            .filter(ScoreEvent.id_persona == persona.id_persona)
            .order_by(ScoreEvent.fecha_creacion.desc())
            .first()
        )

        if not ultimo_score:
            raise HTTPException(status_code=500, detail="No se pudo registrar el score en la base de datos")
        

                # 🔹 9️⃣ Traigo detalle de pólizas activas para mostrar en el front
        from sqlalchemy import text

        query_polizas = """
            SELECT 
                tipo_seguro,
                cobertura,
                suma_asegurada,
                prima_pagada,
                estado
            FROM polizas
            WHERE id_persona = :id_persona AND estado = 'Activa'
        """
        polizas = db.execute(text(query_polizas), {"id_persona": persona.id_persona}).fetchall()
        features["polizas_detalle"] = [dict(row._mapping) for row in polizas]


        # 9️⃣ Devuelvo el resultado completo al front
        return {
            "dni": dni,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "score": ultimo_score.puntaje,
            "nivel": ultimo_score.nivel_score,
            "productos_recomendados": resultado["productos_recomendados"],
            "features": features,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general en obtener_prediccion_por_dni: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
