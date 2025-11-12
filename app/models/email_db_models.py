from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base







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