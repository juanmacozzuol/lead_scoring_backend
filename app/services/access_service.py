# app/services/access_service.py
import os
from datetime import datetime, timedelta
from typing import Optional, Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Importaciones de FastAPI
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer

# Importaciones de la aplicación
from app.database.database import get_db
# Asegúrate de que este import sea correcto según tu estructura de modelos
from app.models.user_db_models import Usuario 



# JWT config
SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-super-secret-key")  # ¡CAMBIA ESTO!
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Esquema de seguridad OAuth2 con flujo de contraseña para la documentación de FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Asume que tienes un endpoint /token

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, clave: str) -> Usuario | None:
    """Retorna el usuario si la autenticación es exitosa, None en caso contrario."""
    user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
    if not user:
        return None
    # 'clave' es la contraseña plana, 'user.clave' es el hash
    if not verify_password(clave, user.clave):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un JWT token con tiempo de expiración."""
    to_encode = data.copy()
    # Usa utcnow() para consistencia con la librería 'jose'
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia PRINCIPAL para obtener el usuario autenticado.
    
    1. Obtiene el token JWT del header 'Authorization: Bearer <token>'.
    2. Decodifica el token y valida la firma.
    3. Busca el usuario en la BD usando el 'sub' (subject/ID) del token.
    4. Levanta HTTPException si falla.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar credenciales o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub") # 'sub' es el estándar para el sujeto (user ID)
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        # Esto atrapa errores de decodificación o expiración
        raise credentials_exception

    # Buscar el usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    if not usuario:
        # Usuario no encontrado a pesar de tener un token válido (ej. fue eliminado)
        raise credentials_exception
    
    print(f"Usuario autenticado por JWT: {usuario.nombre_usuario} (ID={usuario.id_usuario}, Rol={usuario.rol})")
    
    return usuario



def require_role(rol_requerido: str):
    """
    Dependencia opcional que requiere un rol específico.
    
    Uso:
    @router.get("/admin-only")
    def endpoint(user: Usuario = Depends(require_role("admin"))):
        ...
    """
    def verificar_rol(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol != rol_requerido:
            # Puedes usar 403 Forbidden para autorización fallida
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol '{rol_requerido}'. Tu rol es '{current_user.rol}'",
            )
        return current_user
    
    return verificar_rol