from datetime import date, timedelta
from random import randint, choice, random
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine, Base
from app.database.models import Persona, Direccion, Telefono, Producto, Poliza, Pago, Siniestro

# =========================================
# FUNCIONES AUXILIARES
# =========================================
def calcular_edad(fecha_nacimiento):
    today = date.today()
    return today.year - fecha_nacimiento.year - (
        (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )

def asignar_estado_civil(fecha_nacimiento, cantidad_hijos):
    edad = calcular_edad(fecha_nacimiento)
    if edad < 26:
        return "Soltero"
    elif 26 <= edad <= 40:
        return "Casado" if cantidad_hijos > 0 else "Soltero"
    elif 41 <= edad <= 55:
        return "Casado" if cantidad_hijos > 1 else "Divorciado"
    elif 56 <= edad <= 70:
        return "Casado"
    else:
        return "Viudo"

# =========================================
# INICIALIZACIÓN DE DB
# =========================================
Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

# =========================================
# 1️⃣ PRODUCTOS BASE
# =========================================
productos = [
    Producto(nombre="Seguro de Vida", tipo_producto="Vida",
             coberturas_incluidas="Muerte, Invalidez", prima_base=150000),
    Producto(nombre="Seguro de Auto", tipo_producto="Auto",
             coberturas_incluidas="Responsabilidad Civil, Robo, Daños", prima_base=120000),
    Producto(nombre="Seguro de Hogar", tipo_producto="Hogar",
             coberturas_incluidas="Incendio, Robo, Daños", prima_base=180000),
    Producto(nombre="Seguro de Salud", tipo_producto="Salud",
             coberturas_incluidas="Cobertura médica completa", prima_base=100000),
]
db.add_all(productos)
db.commit()
vida, auto, hogar, salud = productos

# =========================================
# 2️⃣ PERSONAS
# =========================================
personas_data = [
    # === CROSS-SELLING ALTO ===
    {"nombre": "María", "apellido": "Gómez", "genero": "Femenino",
     "dni": "28564789", "email": "maria.gomez@example.com",
     "fecha_nacimiento": date(1985, 6, 14), "fecha_registro": date(2014, 5, 10),
     "contacto": "1145236987", "cantidad_hijos": 2, "ocupacion": "Empleado",
     "vivienda_propia": True, "posee_auto": True},

    {"nombre": "Carlos", "apellido": "Fernández", "genero": "Masculino",
     "dni": "23125478", "email": "carlos.fernandez@example.com",
     "fecha_nacimiento": date(1973, 8, 15), "fecha_registro": date(2010, 8, 15),
     "contacto": "1156748390", "cantidad_hijos": 3, "ocupacion": "Empresario",
     "vivienda_propia": True, "posee_auto": True},

    {"nombre": "Lucía", "apellido": "Pérez", "genero": "Femenino",
     "dni": "32456789", "email": "lucia.perez@example.com",
     "fecha_nacimiento": date(1990, 10, 1), "fecha_registro": date(2015, 10, 1),
     "contacto": "1134789502", "cantidad_hijos": 1, "ocupacion": "Empleado",
     "vivienda_propia": True, "posee_auto": True},

    {"nombre": "Jorge", "apellido": "Díaz", "genero": "Masculino",
     "dni": "25789432", "email": "jorge.diaz@example.com",
     "fecha_nacimiento": date(1978, 9, 3), "fecha_registro": date(2012, 3, 20),
     "contacto": "1123945847", "cantidad_hijos": 0, "ocupacion": "Autónomo",
     "vivienda_propia": True, "posee_auto": True},

    # === CROSS-SELLING MEDIO ===
    {"nombre": "Sofía", "apellido": "Martínez", "genero": "Femenino",
     "dni": "37645123", "email": "sofia.martinez@example.com",
     "fecha_nacimiento": date(1993, 2, 17), "fecha_registro": date(2019, 1, 10),
     "contacto": "1145567834", "cantidad_hijos": 0, "ocupacion": "Empleado",
     "vivienda_propia": False, "posee_auto": True},

    {"nombre": "Tomás", "apellido": "Rivas", "genero": "Masculino",
     "dni": "30876543", "email": "tomas.rivas@example.com",
     "fecha_nacimiento": date(1988, 4, 12), "fecha_registro": date(2018, 4, 12),
     "contacto": "1123567890", "cantidad_hijos": 1, "ocupacion": "Autónomo",
     "vivienda_propia": True, "posee_auto": False},

    {"nombre": "Ana", "apellido": "Silva", "genero": "Femenino",
     "dni": "31098765", "email": "ana.silva@example.com",
     "fecha_nacimiento": date(1987, 11, 23), "fecha_registro": date(2016, 11, 23),
     "contacto": "1154678321", "cantidad_hijos": 2, "ocupacion": "Empleado",
     "vivienda_propia": True, "posee_auto": True},

    {"nombre": "Ricardo", "apellido": "Mendoza", "genero": "Masculino",
     "dni": "29786543", "email": "ricardo.mendoza@example.com",
     "fecha_nacimiento": date(1982, 2, 5), "fecha_registro": date(2018, 2, 5),
     "contacto": "1134786521", "cantidad_hijos": 0, "ocupacion": "Autónomo",
     "vivienda_propia": False, "posee_auto": True},

    # === CROSS-SELLING BAJO ===
    {"nombre": "Laura", "apellido": "Sánchez", "genero": "Femenino",
     "dni": "43897654", "email": "laura.sanchez@example.com",
     "fecha_nacimiento": date(2002, 5, 1), "fecha_registro": date(2024, 5, 1),
     "contacto": "1133345566", "cantidad_hijos": 0, "ocupacion": "Estudiante",
     "vivienda_propia": False, "posee_auto": False},

    {"nombre": "Pedro", "apellido": "Juárez", "genero": "Masculino",
     "dni": "19234567", "email": "pedro.juarez@example.com",
     "fecha_nacimiento": date(1962, 3, 14), "fecha_registro": date(2010, 3, 14),
     "contacto": "1167889011", "cantidad_hijos": 0, "ocupacion": "Desempleado",
     "vivienda_propia": False, "posee_auto": True},

    {"nombre": "Carolina", "apellido": "Ruiz", "genero": "Femenino",
     "dni": "39645382", "email": "carolina.ruiz@example.com",
     "fecha_nacimiento": date(1998, 10, 22), "fecha_registro": date(2023, 10, 22),
     "contacto": "1144455566", "cantidad_hijos": 1, "ocupacion": "Empleado",
     "vivienda_propia": True, "posee_auto": False},

    {"nombre": "Hernán", "apellido": "Vega", "genero": "Masculino",
     "dni": "45623789", "email": "hernan.vega@example.com",
     "fecha_nacimiento": date(2000, 7, 10), "fecha_registro": date(2024, 7, 10),
     "contacto": "1122334455", "cantidad_hijos": 0, "ocupacion": "Estudiante",
     "vivienda_propia": False, "posee_auto": False},
]

# Asignar estado civil automáticamente según edad e hijos
for data in personas_data:
    fn = data["fecha_nacimiento"]
    hijos = data.get("cantidad_hijos", 0)
    data["estado_civil"] = asignar_estado_civil(fn, hijos)

personas = [Persona(**data) for data in personas_data]
db.add_all(personas)
db.commit()

# =========================================
# 3️⃣ DIRECCIONES Y TELÉFONOS
# =========================================
direcciones_reales = [
    ("Av. Santa Fe", "2456", "CABA", "Buenos Aires"),
    ("Bv. San Juan", "1200", "Córdoba", "Córdoba"),
    ("Av. Pellegrini", "3210", "Rosario", "Santa Fe"),
    ("Calle Las Heras", "875", "Mendoza", "Mendoza"),
    ("Av. Colón", "985", "Mar del Plata", "Buenos Aires"),
    ("San Martín", "203", "Salta", "Salta"),
    ("Moreno", "412", "Bahía Blanca", "Buenos Aires"),
    ("Av. Alem", "650", "Tucumán", "Tucumán"),
    ("Belgrano", "785", "Resistencia", "Chaco"),
    ("Mitre", "2231", "San Miguel de Tucumán", "Tucumán"),
    ("Rivadavia", "340", "La Plata", "Buenos Aires"),
    ("Urquiza", "1578", "Neuquén", "Neuquén"),
]

for p, d in zip(personas, direcciones_reales):
    direccion = Direccion(
        calle=d[0], numero=d[1], ciudad=d[2], provincia=d[3],
        pais="Argentina", cod_postal="1000", id_persona=p.id_persona
    )
    telefono = Telefono(numero=f"11{p.dni[-6:]}", tipo="Celular", id_persona=p.id_persona)
    db.add_all([direccion, telefono])
db.commit()

# =========================================
# 4️⃣ PÓLIZAS, PAGOS Y SINIESTROS
# =========================================
for p in personas:
    cantidad_polizas = randint(1, 3)
    productos_asignados = [choice([vida, auto, hogar, salud]) for _ in range(cantidad_polizas)]

    for producto in productos_asignados:
        poliza = Poliza(
            nro_poliza=f"POL-{p.dni[-4:]}-{randint(1000,9999)}",
            tipo_seguro=producto.tipo_producto,
            fecha_inicio=date(2022, randint(1, 12), randint(1, 28)),
            fecha_vencimiento=date(2025, randint(1, 12), randint(1, 28)),
            estado="Activa",
            suma_asegurada=producto.prima_base * randint(50, 150),
            prima_pagada=producto.prima_base,
            cobertura=producto.coberturas_incluidas,
            id_persona=p.id_persona,
            id_producto=producto.id_producto,
        )
        db.add(poliza)
        db.flush()

        # Probabilidad de impago según ocupación
        estado_pago = "Pagado"
        if (p.ocupacion == "Desempleado" and random() < 0.3) or \
           (p.ocupacion == "Autónomo" and random() < 0.2) or \
           (p.ocupacion == "Empleado" and random() < 0.15) or \
           (p.ocupacion == "Estudiante" and random() < 0.1):
            estado_pago = "Impago"

        pago = Pago(
            fecha_pago=date.today() - timedelta(days=randint(5, 30)),
            monto=producto.prima_base,
            forma_pago="Débito automático",
            estado_pago=estado_pago,
            id_poliza=poliza.id_poliza,
        )
        db.add(pago)

        # Siniestros coherentes
        if producto.tipo_producto in ["Auto", "Hogar"] and random() < 0.25:
            siniestro = Siniestro(
                fecha_reporte=date.today() - timedelta(days=randint(30, 730)),
                tipo_siniestro="Robo" if producto.tipo_producto == "Auto" else "Incendio",
                monto_reclamado=randint(200000, 800000),
                estado="Cerrado" if random() > 0.5 else "Abierto",
                id_poliza=poliza.id_poliza,
            )
            db.add(siniestro)

db.commit()
db.close()
