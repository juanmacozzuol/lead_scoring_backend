# app/controllers/access_controller.py

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.services.access_service import authenticate_user, create_access_token, get_password_hash
from app.models.user_db_models import Usuario
from app.database import get_db

def login_user(username: str, clave: str, db: Session = Depends(get_db)):
    """Handles user login flow."""
    user = authenticate_user(db, username, clave)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(data={"sub": user.nombre_usuario})
    return {"access_token": access_token, "token_type": "bearer"}


def register_user(username: str, clave: str, email: str | None = None, db: Session = Depends(get_db)):
    """Handles new user registration."""
    existing_user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
   

    hashed_password = get_password_hash(clave)
    new_user = Usuario(nombre_usuario=username, clave=hashed_password, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User '{username}' registered successfully"}
