from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base




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



