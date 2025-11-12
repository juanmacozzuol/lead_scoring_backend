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

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    clave = Column(String(200), nullable=False)  
    email = Column(String(100), unique=True)
    rol = Column(String(20))

    correos = relationship("Correo", back_populates="usuario")