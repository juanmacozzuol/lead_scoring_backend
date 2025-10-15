from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Persona(Base):
    __tablename__ = "personas"

    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String(20))
    dni = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True)
    fecha_registro = Column(Date)
    contacto = Column(String(50))
    cantidad_hijos = Column(Integer, default=0)
    estado_civil = Column(String(20), nullable=False, default="Soltero")
    ocupacion = Column(String(50))
    vivienda_propia = Column(Boolean, default=False)  
    posee_auto = Column(Boolean, default=False)       

    direcciones = relationship("Direccion", back_populates="persona", cascade="all, delete-orphan")
    telefonos = relationship("Telefono", back_populates="persona", cascade="all, delete-orphan")
    polizas = relationship("Poliza", back_populates="persona", cascade="all, delete-orphan")
    scorings = relationship("ScoreEvent", back_populates="persona", cascade="all, delete-orphan")
    correos = relationship("Correo", back_populates="persona", cascade="all, delete-orphan")


class Direccion(Base):
    __tablename__ = "direccion"

    id_direccion = Column(Integer, primary_key=True)
    calle = Column(String(100))
    numero = Column(String(10))
    ciudad = Column(String(50))
    provincia = Column(String(50))
    pais = Column(String(50))
    cod_postal = Column(String(20))
    id_persona = Column(Integer, ForeignKey("personas.id_persona"))

    persona = relationship("Persona", back_populates="direcciones")


class Telefono(Base):
    __tablename__ = "telefono"

    id_telefono = Column(Integer, primary_key=True)
    numero = Column(String(20))
    tipo = Column(String(20))
    id_persona = Column(Integer, ForeignKey("personas.id_persona"))

    persona = relationship("Persona", back_populates="telefonos")


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo_producto = Column(String(50))
    coberturas_incluidas = Column(String(200))
    prima_base = Column(Float)

    polizas = relationship("Poliza", back_populates="producto")
    correos = relationship("Correo", back_populates="producto")


class Poliza(Base):
    __tablename__ = "polizas"

    id_poliza = Column(Integer, primary_key=True)
    nro_poliza = Column(String(50), unique=True)
    tipo_seguro = Column(String(50))
    fecha_inicio = Column(Date)
    fecha_vencimiento = Column(Date)
    estado = Column(String(20))
    suma_asegurada = Column(Float)
    prima_pagada = Column(Float)
    cobertura = Column(String(100))
    id_persona = Column(Integer, ForeignKey("personas.id_persona"))
    id_producto = Column(Integer, ForeignKey("productos.id_producto"))

    persona = relationship("Persona", back_populates="polizas")
    producto = relationship("Producto", back_populates="polizas")
    siniestros = relationship("Siniestro", back_populates="poliza", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="poliza", cascade="all, delete-orphan")


class Siniestro(Base):
    __tablename__ = "siniestros"

    id_siniestro = Column(Integer, primary_key=True)
    fecha_reporte = Column(Date)
    tipo_siniestro = Column(String(50))
    monto_reclamado = Column(Float)
    estado = Column(String(20))
    id_poliza = Column(Integer, ForeignKey("polizas.id_poliza"))

    poliza = relationship("Poliza", back_populates="siniestros")


class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True)
    fecha_pago = Column(Date)
    monto = Column(Float)
    forma_pago = Column(String(50))
    estado_pago = Column(String(20))
    id_poliza = Column(Integer, ForeignKey("polizas.id_poliza"))

    poliza = relationship("Poliza", back_populates="pagos")


class ScoreEvent(Base):
    __tablename__ = "score_event"

    id_score = Column(Integer, primary_key=True)
    puntaje = Column(Float)
    nivel_score = Column(String(20))
    fecha_creacion = Column(Date)
    id_persona = Column(Integer, ForeignKey("personas.id_persona"))

    persona = relationship("Persona", back_populates="scorings")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    clave = Column(String(200), nullable=False)  
    email = Column(String(100), unique=True)
    rol = Column(String(20))

    correos = relationship("Correo", back_populates="usuario")


class Correo(Base):
    __tablename__ = "correo"

    id_correo = Column(Integer, primary_key=True)
    asunto = Column(String(200))
    cuerpo = Column(String(500))
    fecha_creacion = Column(Date)
    fecha_envio = Column(Date)
    id_persona = Column(Integer, ForeignKey("personas.id_persona"))
    id_producto = Column(Integer, ForeignKey("productos.id_producto"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))

    persona = relationship("Persona", back_populates="correos")
    producto = relationship("Producto", back_populates="correos")
    usuario = relationship("Usuario", back_populates="correos")
