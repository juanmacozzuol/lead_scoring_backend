from datetime import date
from app.database.database import SessionLocal, Base, engine
from app.models.user_db_models import Persona, Direccion, Telefono
from app.models.insurance_db_models import Producto, Poliza, Pago, Siniestro

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# =========================
# PRODUCTOS
# =========================
vida = Producto(nombre="Seguro de Vida", tipo_producto="vida", coberturas_incluidas="Muerte, Invalidez", prima_base=150000)
auto = Producto(nombre="Seguro de Auto", tipo_producto="auto", coberturas_incluidas="Responsabilidad Civil, Robo, Daños", prima_base=120000)
hogar = Producto(nombre="Seguro de Hogar", tipo_producto="hogar", coberturas_incluidas="Incendio, Robo, Daños", prima_base=180000)
salud = Producto(nombre="Seguro de Salud", tipo_producto="salud", coberturas_incluidas="Cobertura médica completa", prima_base=100000)
db.add_all([vida, auto, hogar, salud])
db.commit()

# =========================
# PERSONAS
# =========================
personas = [
    Persona(nombre="Mariana", apellido="Sosa", genero="Femenino", dni="30555444", email="mariana.sosa@example.com",
            fecha_nacimiento=date(1986, 4, 15), fecha_registro=date(2016, 3, 10),
            contacto="correo", cantidad_hijos=2, ocupacion="Empleado", vivienda_propia=True, posee_auto=True, estado_civil="Casado"),
    Persona(nombre="Hernán", apellido="Lopez", genero="Masculino", dni="28777888", email="hernan.lopez@example.com",
            fecha_nacimiento=date(1978, 8, 21), fecha_registro=date(2015, 2, 5),
            contacto="teléfono", cantidad_hijos=1, ocupacion="Autónomo", vivienda_propia=True, posee_auto=True, estado_civil="Casado"),
    Persona(nombre="Camila", apellido="Torres", genero="Femenino", dni="33999666", email="camila.torres@example.com",
            fecha_nacimiento=date(1992, 11, 9), fecha_registro=date(2023, 2, 10),
            contacto="correo", cantidad_hijos=0, ocupacion="Empleado", vivienda_propia=False, posee_auto=True, estado_civil="Soltero"),
    Persona(nombre="Nicolás", apellido="Ramos", genero="Masculino", dni="33222555", email="nicolas.ramos@example.com",
            fecha_nacimiento=date(1989, 3, 30), fecha_registro=date(2022, 1, 10),
            contacto="teléfono", cantidad_hijos=1, ocupacion="Autónomo", vivienda_propia=True, posee_auto=False, estado_civil="Casado"),
    Persona(nombre="Lucía", apellido="Fernandez", genero="Femenino", dni="45444888", email="lucia.fernandez@example.com",
            fecha_nacimiento=date(2001, 9, 25), fecha_registro=date(2023, 1, 20),
            contacto="correo", cantidad_hijos=0, ocupacion="Estudiante", vivienda_propia=False, posee_auto=False, estado_civil="Soltero"),
    Persona(nombre="Carlos", apellido="Medina", genero="Masculino", dni="45999333", email="carlos.medina@example.com",
            fecha_nacimiento=date(1982, 5, 5), fecha_registro=date(2022, 6, 1),
            contacto="teléfono", cantidad_hijos=1, ocupacion="Desempleado", vivienda_propia=False, posee_auto=True, estado_civil="Divorciado"),
]
db.add_all(personas)
db.commit()

# =========================
# FUNCIONES AUXILIARES
# =========================
def crear_poliza(persona, producto, estado_pago="Pagado", siniestros=0, impagos=0):
    poliza = Poliza(
        nro_poliza=f"POL-{persona.dni[-4:]}-{producto.tipo_producto.upper()}",
        tipo_seguro=producto.tipo_producto,
        fecha_inicio=date(2022, 1, 1),
        fecha_vencimiento=date(2025, 1, 1),
        estado="Activa",
        suma_asegurada=producto.prima_base * 100,
        prima_pagada=producto.prima_base,
        cobertura=producto.coberturas_incluidas,
        id_persona=persona.id_persona,
        id_producto=producto.id_producto,
    )
    db.add(poliza)
    db.flush()

    # pagos impagos
    for i in range(max(impagos, 1)):
        estado = "Impago" if i < impagos else estado_pago
        db.add(Pago(fecha_pago=date(2024, 6, 10), monto=producto.prima_base, forma_pago="Débito automático",
                    estado_pago=estado, id_poliza=poliza.id_poliza))

    # siniestros
    for _ in range(siniestros):
        db.add(Siniestro(fecha_reporte=date(2024, 3, 15), tipo_siniestro="Robo",
                         monto_reclamado=300000, estado="Cerrado", id_poliza=poliza.id_poliza))

# =========================
# ASIGNACIONES
# =========================
# Altos
crear_poliza(personas[0], auto, estado_pago="Pagado")  # Mariana
crear_poliza(personas[1], vida, estado_pago="Pagado")  # Hernán

# Medios
crear_poliza(personas[2], auto, estado_pago="Impago", impagos=2)   # Camila
crear_poliza(personas[3], hogar, estado_pago="Pagado", siniestros=2)  # Nicolás

# Bajos
crear_poliza(personas[4], salud, estado_pago="Impago", impagos=6)  # Lucía
crear_poliza(personas[5], auto, estado_pago="Impago", siniestros=3, impagos=3)  # Carlos

db.commit()
db.close()

print("✅ SEED FINAL cargado correctamente (2 Altos, 2 Medios, 2 Bajos con reglas realistas).")
