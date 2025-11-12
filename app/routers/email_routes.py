from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importamos dependencias de la app
from app.database.database import get_db 
from app.services.access_service import get_current_user
from app.models.user_db_models import Usuario

# Importamos los servicios y repositorios que usaremos
from app.services import email_service
from app.repositories import correo_repository

# Importamos todos los modelos Pydantic
from app.models.email_models import (
    GenerarBorradorRequest,
    GenerarBorradorResponse,
    EnviarCorreoRequest,
    EnviarCorreoResponse,
    CorreoGuardadoCreate,
    CorreoGuardadoUpdate,
    CorreoGuardadoResponse,
    CorreoHistorialResponse
)

# Creamos un router especifico para esta logica
router = APIRouter(
    prefix="/correos", # Todas las rutas empezaran con /correos
    tags=["Correos y Favoritos"] # Etiqueta para la documentacion de la API
)


# Generacion y envio

@router.post(
    "/ia/generar-borrador",
    response_model=GenerarBorradorResponse,
    summary="Generar borrador de email con IA",
    description="""
    Genera un borrador personalizado usando IA.
    
    El sistema analiza:
    - Perfil completo del cliente (edad, ocupación, situación familiar)
    - Características del producto
    - Etapa de la relación comercial
    - Tono deseado
    
    Importante: Esta operación puede tardar un tiempo dependiendo el modelo.
    
    Etapas válidas: prospecto, cliente_activo, cliente_inactivo
    
    Tonos válidos: muy_formal, neutral, informal
    """,
    responses={
        200: {"description": "Borrador generado exitosamente"},
        404: {"description": "Cliente o producto no encontrado"},
        500: {"description": "Error del servicio de IA"},
        503: {"description": "Servicio de IA no disponible"}
    }
)

def generar_borrador(
    req: GenerarBorradorRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Requerido para auditoria futura
):
    """
    Toma los datos del cliente/producto y un tono,
    y pide al motor LLM (Google, OpenAI o Local) que genere un borrador.
    
    ESTA LLAMADA ES LENTA (puede tardar dependiendo el modelo).
    """
    # La logica esta en el servicio
    return email_service.generar_borrador_ia(db=db, req=req)


@router.post(
    "/ia/enviar-correo", 
    response_model=EnviarCorreoResponse, 
    summary="Enviar un correo (generado por IA y editado)"
)
def enviar_correo(
    req: EnviarCorreoRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Envia el email con el asunto y cuerpo exactos provistos (ad-hoc).
    Esta es la funcion final de envio.
    """
    # La logica esta en el servicio
    return email_service.enviar_correo_adhoc(db=db, req=req, current_user=current_user)


# Gestion de correos guardados

@router.post(
    "/favoritos",
    response_model=CorreoGuardadoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar un correo generado como Favorito"
)
def crear_favorito(
    data: CorreoGuardadoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Guarda el contenido de un correo (asunto/cuerpo) como un
    "favorito" personal para el empleado logueado.
    """
    return email_service.crear_correo_guardado(db=db, data=data, current_user=current_user)


@router.get(
    "/favoritos/producto/{id_producto}", 
    response_model=List[CorreoGuardadoResponse], 
    summary="Listar mis Favoritos para un producto"
)
def obtener_mis_favoritos_por_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Devuelve una lista de todos los "favoritos" que el empleado
    logueado ha guardado para un producto especifico.
    """
    return email_service.obtener_correos_guardados_por_producto(
        db=db, id_producto=id_producto, id_usuario=current_user.id_usuario
    )


@router.put(
    "/favoritos/{id_correo_guardado}", 
    response_model=CorreoGuardadoResponse, 
    summary="Actualizar un Favorito"
)
def actualizar_favorito(
    id_correo_guardado: int,
    data: CorreoGuardadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza el nombre, asunto o cuerpo de un favorito.
    Valida que el favorito pertenezca al usuario logueado.
    """
    return email_service.actualizar_correo_guardado(
        db=db, id_correo_guardado=id_correo_guardado, data=data, id_usuario=current_user.id_usuario
    )


@router.delete(
    "/favoritos/{id_correo_guardado}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un Favorito"
)
def eliminar_favorito(
    id_correo_guardado: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un favorito.
    Valida que el favorito pertenezca al usuario logueado.
    """
    email_service.eliminar_correo_guardado(
        db=db, id_correo_guardado=id_correo_guardado, id_usuario=current_user.id_usuario
    )
    # Devuelve 204 No Content, que no tiene cuerpo de respuesta


# Historial de correos

@router.get(
    "/historial/persona/{id_persona}", 
    response_model=List[CorreoHistorialResponse],
    summary="Ver historial de correos enviados a un cliente"
)
def obtener_historial_por_persona(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Para asegurar que este logueado
):
    """
    Obtiene el historial de correos (desde la tabla Correo) enviados
    a un cliente (Persona) especifico.
    """
    # Esta logica esta en el repositorio
    return correo_repository.obtener_historial_por_persona(db=db, id_persona=id_persona)