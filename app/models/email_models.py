from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Modelos para Generacion y Envio de Correos
class GenerarBorradorRequest(BaseModel):
    """
    Datos que necesitamos del frontend para pedir un borrador a la IA.
    """
    id_persona: int
    id_producto: int
    formalidad: str
    etapa_relacion: str

class GenerarBorradorResponse(BaseModel):
    """
    El JSON que la IA (o nuestro servicio) devuelve al frontend.
    """
    asunto_sugerido: str
    cuerpo_sugerido: str

class EnviarCorreoRequest(BaseModel):
    """
    Datos que envia el frontend para el envio final.
    Es el texto "ad-hoc", ya editado por el empleado.
    """
    id_persona: int
    id_producto: int  # Lo necesitamos para el log de auditoria
    asunto: str
    cuerpo: str       # El HTML/texto final

class EnviarCorreoResponse(BaseModel):
    """
    Respuesta simple de exito tras enviar el correo.
    """
    status: str
    mensaje: str
    id_correo_log: int # El ID del registro en la tabla 'Correo'


# Modelos para "Correos Guardados"
class CorreoGuardadoBase(BaseModel):
    """
    Campos comunes que definen un favorito.
    """
    nombre: str
    asunto: str
    cuerpo: str

class CorreoGuardadoCreate(CorreoGuardadoBase):
    """
    Datos que necesitamos para CREAR un nuevo favorito.
    (El id_usuario vendra del token).
    """
    id_producto: int

class CorreoGuardadoUpdate(CorreoGuardadoBase):
    """
    Datos que permitimos ACTUALIZAR de un favorito.
    (No permitimos cambiar el producto al que esta asociado).
    """
    pass

class CorreoGuardadoResponse(CorreoGuardadoBase):
    """
    Datos completos de un favorito que devolvemos al frontend.
    """
    id_correo_guardado: int
    id_producto: int
    id_usuario: int

    class Config:
        from_attributes = True # Para que Pydantic lea el modelo de SQLAlchemy



# Modelos para el Historial
class CorreoHistorialResponse(BaseModel):
    """
    Representa una fila de la tabla 'Correo' (historial de enviados).
    """
    id_correo: int
    asunto: str
    cuerpo: str
    fecha_creacion: date
    fecha_envio: Optional[date]
    id_persona: int
    id_producto: int
    id_usuario: int
    dni: str
    mail: str          # email de la persona (destinatario)
    usuario: str       # nombre del usuario que envió el correo

    class Config:
        from_attributes = True # Para que Pydantic lea el modelo de SQLAlchemy