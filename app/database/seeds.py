from datetime import date
from app.database.database import SessionLocal, Base, engine
from app.models.user_db_models import Persona, Direccion, Telefono, Usuario
from app.models.insurance_db_models import Producto, Poliza, Pago, Siniestro
from app.models.email_db_models import Correo

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# =========================
# PRODUCTOS
# =========================
vida = Producto(
    nombre="Seguro de Vida",
    tipo_producto="vida",
    coberturas_incluidas="Muerte, Invalidez",
    prima_base=150000
)
auto = Producto(
    nombre="Seguro de Auto",
    tipo_producto="auto",
    coberturas_incluidas="Responsabilidad Civil, Robo, Daños",
    prima_base=120000
)
hogar = Producto(
    nombre="Seguro de Hogar",
    tipo_producto="hogar",
    coberturas_incluidas="Incendio, Robo, Daños",
    prima_base=180000
)
salud = Producto(
    nombre="Seguro de Salud",
    tipo_producto="salud",
    coberturas_incluidas="Cobertura médica completa",
    prima_base=100000
)

db.add_all([vida, auto, hogar, salud])
db.commit()

# =========================
# PERSONAS (5 ALTOS, 5 MEDIOS, 5 BAJOS)
# =========================
personas = [
    # ===== ALTOS =====
    Persona(
        nombre="Mariana",
        apellido="Sosa",
        genero="Femenino",
        dni="30555444",
        email="mariana.sosa@example.com",
        fecha_nacimiento=date(1986, 4, 15),
        fecha_registro=date(2016, 3, 10),
        contacto="correo",
        cantidad_hijos=2,
        ocupacion="Empleado",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Hernán",
        apellido="Lopez",
        genero="Masculino",
        dni="28777888",
        # mail pedido para probar score alto
        email="angy9817.am@gmail.com",
        fecha_nacimiento=date(1978, 8, 21),
        fecha_registro=date(2015, 2, 5),
        contacto="teléfono",
        cantidad_hijos=1,
        ocupacion="Autónomo",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Soledad",
        apellido="Prieto",
        genero="Femenino",
        dni="31234567",
        email="soledad.prieto@example.com",
        fecha_nacimiento=date(1985, 6, 11),
        fecha_registro=date(2014, 4, 3),
        contacto="correo",
        cantidad_hijos=2,
        ocupacion="Empleado",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Juan Marcos",
        apellido="Cozzuol",
        genero="Masculino",
        dni="27894561",
        email="juanmacozzuol@gmail.com",
        fecha_nacimiento=date(1983, 9, 20),
        fecha_registro=date(2013, 3, 1),
        contacto="correo",
        cantidad_hijos=1,
        ocupacion="Empresario",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Laura",
        apellido="Castillo",
        genero="Femenino",
        dni="29567812",
        email="laura.castillo@example.com",
        fecha_nacimiento=date(1987, 1, 8),
        fecha_registro=date(2016, 6, 18),
        contacto="correo",
        cantidad_hijos=0,
        ocupacion="Empleado",
        vivienda_propia=True,
        posee_auto=False,
        estado_civil="Soltero"
    ),

    # ===== MEDIOS =====
    Persona(
        nombre="Camila",
        apellido="Torres",
        genero="Femenino",
        dni="33999666",
        email="camila.torres@example.com",
        fecha_nacimiento=date(1992, 11, 9),
        fecha_registro=date(2024, 2, 10),
        contacto="correo",
        cantidad_hijos=0,
        ocupacion="Empleado",
        vivienda_propia=False,
        posee_auto=True,
        estado_civil="Soltero"
    ),
    Persona(
        nombre="Nicolás",
        apellido="Ramos",
        genero="Masculino",
        dni="33222555",
        email="nicolas.ramos@example.com",
        fecha_nacimiento=date(1989, 3, 30),
        fecha_registro=date(2016, 1, 10),
        contacto="teléfono",
        cantidad_hijos=1,
        ocupacion="Autónomo",
        vivienda_propia=True,
        posee_auto=False,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Matías",
        apellido="Luna",
        genero="Masculino",
        dni="32789123",
        email="matias.luna@example.com",
        fecha_nacimiento=date(1990, 1, 19),
        fecha_registro=date(2012, 7, 15),
        contacto="correo",
        cantidad_hijos=0,
        ocupacion="Autónomo",
        vivienda_propia=False,
        posee_auto=True,
        estado_civil="Soltero"
    ),
    Persona(
        nombre="Camila",
        apellido="Beraldo",
        genero="Femenino",
        dni="34987651",
        email="camilasberaldo@hotmail.com",
        fecha_nacimiento=date(1995, 8, 19),
        fecha_registro=date(2017, 11, 30),
        contacto="correo",
        cantidad_hijos=1,
        ocupacion="Empleado",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),
    Persona(
        nombre="Sergio",
        apellido="Alvarez",
        genero="Masculino",
        dni="33124567",
        email="sergio.alvarez@example.com",
        fecha_nacimiento=date(1988, 10, 2),
        fecha_registro=date(2010, 5, 12),
        contacto="teléfono",
        cantidad_hijos=2,
        ocupacion="Empleado",
        vivienda_propia=True,
        posee_auto=True,
        estado_civil="Casado"
    ),

    # ===== BAJOS =====
    Persona(
        nombre="Lucía",
        apellido="Fernandez",
        genero="Femenino",
        dni="45444888",
        email="lucia.fernandez@example.com",
        fecha_nacimiento=date(2001, 9, 25),
        fecha_registro=date(2023, 1, 20),
        contacto="correo",
        cantidad_hijos=0,
        ocupacion="Estudiante",
        vivienda_propia=False,
        posee_auto=False,
        estado_civil="Soltero"
    ),
    Persona(
        nombre="Carlos",
        apellido="Medina",
        genero="Masculino",
        dni="45999333",
        email="carlos.medina@example.com",
        fecha_nacimiento=date(1982, 5, 5),
        fecha_registro=date(2024, 6, 1),
        contacto="teléfono",
        cantidad_hijos=1,
        ocupacion="Desempleado",
        vivienda_propia=False,
        posee_auto=True,
        estado_civil="Divorciado"
    ),
    Persona(
        nombre="Jorge",
        apellido="Díaz",
        genero="Masculino",
        dni="24123456",
        email="jorge.diaz@example.com",
        fecha_nacimiento=date(1970, 2, 3),
        fecha_registro=date(2018, 5, 20),
        contacto="teléfono",
        cantidad_hijos=3,
        ocupacion="Desempleado",
        vivienda_propia=False,
        posee_auto=True,
        estado_civil="Divorciado"
    ),
    Persona(
        nombre="Pablo",
        apellido="Benítez",
        genero="Masculino",
        dni="24567891",
        email="pablo.benitez@example.com",
        fecha_nacimiento=date(1975, 3, 23),
        fecha_registro=date(2019, 9, 2),
        contacto="correo",
        cantidad_hijos=2,
        ocupacion="Desempleado",
        vivienda_propia=False,
        posee_auto=True,
        estado_civil="Divorciado"
    ),
    Persona(
        nombre="Romina",
        apellido="Flores",
        genero="Femenino",
        dni="40234567",
        email="romina.flores@example.com",
        fecha_nacimiento=date(1998, 7, 15),
        fecha_registro=date(2024, 3, 10),
        contacto="correo",
        cantidad_hijos=0,
        ocupacion="Estudiante",
        vivienda_propia=False,
        posee_auto=False,
        estado_civil="Soltero"
    ),
]

db.add_all(personas)
db.commit()

# =========================
# FUNCIÓN AUXILIAR
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

    # pagos (impagos vs pagado final)
    for i in range(max(impagos, 1)):
        estado = "Impago" if i < impagos else estado_pago
        db.add(
            Pago(
                fecha_pago=date(2024, 6, 10),
                monto=producto.prima_base,
                forma_pago="Débito automático",
                estado_pago=estado,
                id_poliza=poliza.id_poliza,
            )
        )

    # siniestros
    for _ in range(siniestros):
        db.add(
            Siniestro(
                fecha_reporte=date(2024, 3, 15),
                tipo_siniestro="Robo",
                monto_reclamado=300000,
                estado="Cerrado",
                id_poliza=poliza.id_poliza,
            )
        )

# =========================
# ASIGNACIONES DE PÓLIZAS
# =========================
# Índices de ayuda
mariana, hernan, soledad, juan, laura = personas[0:5]
camila_t, nicolas, matias, camila_b, sergio = personas[5:10]
lucia, carlos, jorge, pablo, romina = personas[10:15]

# ------- ALTOS (sin impagos, sin siniestros) -------
# Varios con más de una póliza
crear_poliza(mariana, auto, estado_pago="Pagado")
crear_poliza(mariana, hogar, estado_pago="Pagado")

crear_poliza(hernan, vida, estado_pago="Pagado")
crear_poliza(hernan, auto, estado_pago="Pagado")

crear_poliza(soledad, hogar, estado_pago="Pagado")

crear_poliza(juan, auto, estado_pago="Pagado")
crear_poliza(juan, vida, estado_pago="Pagado")

crear_poliza(laura, salud, estado_pago="Pagado")
crear_poliza(laura, vida, estado_pago="Pagado")

# ------- MEDIOS (1–2 impagos y/o 1 siniestro) -------
crear_poliza(camila_t, auto, estado_pago="Pagado", impagos=4)              # 2 impagos
crear_poliza(nicolas, hogar, estado_pago="Pagado", siniestros=1, impagos=1)  # 1 siniestro + 1 impago
crear_poliza(matias, auto, estado_pago="Pagado", siniestros=1)                # 2 impagos
crear_poliza(camila_b, vida, estado_pago="Pagado", impagos=2)              # 1 impago
crear_poliza(sergio, auto, estado_pago="Pagado", siniestros=1, impagos=2)  # 1 siniestro + 1 impago

# ------- BAJOS (muchas impagas / perfil riesgoso) -------
crear_poliza(lucia, salud, estado_pago="Impago", impagos=6)                # >3 impagas
crear_poliza(carlos, auto, estado_pago="Impago", siniestros=2, impagos=4)  # 1 siniestro + 4 impagas
crear_poliza(jorge, auto, estado_pago="Impago", siniestros=1, impagos=6)   # 1 siniestro + 4 impagas
crear_poliza(pablo, auto, estado_pago="Impago", impagos=5)                 # 5 impagas
crear_poliza(romina, salud, estado_pago="Impago", impagos=4)               # 4 impagas

db.commit()
db.close()

print("✅ SEED FINAL cargado correctamente).")
