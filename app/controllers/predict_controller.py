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


# =============================
# FUNCIONES AUXILIARES
# =============================

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


# =============================
# CONTROLADOR PRINCIPAL
# =============================

def obtener_prediccion_por_dni(dni: str, db):
    persona = obtener_persona_por_dni(db, dni)
    if not persona:
        raise HTTPException(status_code=404, detail="No se encontró ninguna persona con ese DNI")

    print("\n✅ PERSONA ENCONTRADA EN BD:")
    print(dict(persona._mapping))

    # === CÁLCULOS AUXILIARES ===
    edad = calcular_edad(persona.fecha_nacimiento)
    antiguedad = calcular_antiguedad(persona.fecha_registro)
    provincia = obtener_provincia_por_persona(db, persona.id_persona) or "Buenos Aires"

    # === DATOS RELACIONADOS ===
    poliza_data = obtener_estadisticas_polizas(db, persona.id_persona)
    siniestro_data = obtener_estadisticas_siniestros(db, persona.id_persona)
    productos = obtener_tipos_productos_por_persona(db, persona.id_persona)
    cuotas_impagas = obtener_cantidad_cuotas_impagas_por_persona(db, persona.id_persona)

    # === MAPEO DE PRODUCTOS ===
    tiene_auto = int("auto" in productos)
    tiene_hogar = int("hogar" in productos)
    tiene_vida = int("vida" in productos)
    tiene_salud = int("salud" in productos)

    # === FEATURES PARA EL MODELO ===
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

    print("\n📊 FEATURES CALCULADAS (FINAL):")
    for k, v in features.items():
        print(f" - {k}: {v}")

    # === PREDICCIÓN ===
    resultado = predecir_cross_selling(features)

    print("\n🤖 RESULTADO DEL MODELO:")
    print(resultado)

    return {
        "dni": dni,
        "score": resultado["score"],
        "nivel": resultado["nivel"],
        "productos_recomendados": resultado["productos_recomendados"],
        "features": features,
    }
