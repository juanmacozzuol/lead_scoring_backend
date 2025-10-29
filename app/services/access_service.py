# IMPORTANTE:
# Este archivo access_service.py fue creado para pruebas, se debe sumar logica JWT antes de hacer mergear

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.database.models import Usuario


def get_current_user(
    x_user_id: Optional[int] = Header(None),  # Leer ID del header
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia SIMPLE para obtener el usuario.
    
    Lee el ID del usuario desde el header 'X-User-Id'.
    
    Esto es TEMPORAL para desarrollo y pruebas.
    """
    
    # Si no se proporciona el header, usar un usuario por defecto
    if x_user_id is None:
        # Usar usuario por defecto (ID=1)
        # Puedes cambiarlo al ID del usuario que tengas en tu BD
        print("No se proporcionó X-User-Id, usando usuario por defecto (ID=1)")
        x_user_id = 1
    
    # Buscar el usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id_usuario == x_user_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID={x_user_id} no encontrado en la base de datos. "
                   f"Verifica que el usuario exista en tu MySQL."
        )
    
    print(f"Usuario autenticado: {usuario.nombre_usuario} (ID={usuario.id_usuario}, Rol={usuario.rol})")
    
    return usuario


def require_role(rol_requerido: str):
    """
    Dependencia opcional para verificar roles.
    
    Uso:
    @router.get("/admin-only")
    def endpoint(user: Usuario = Depends(require_role("admin"))):
        ...
    """
    def verificar_rol(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol != rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol '{rol_requerido}'. Tu rol es '{current_user.rol}'"
            )
        return current_user
    
    return verificar_rol