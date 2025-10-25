# app/routers/access_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.access_controller import register_user, login_user
from app.database import get_db
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    clave: str
    email: str | None = None

class LoginRequest(BaseModel):
    username: str
    clave: str

router = APIRouter(tags=["Access Operations"])



@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Login route using JSON input."""
    return login_user(data.username, data.clave, db)


@router.post("/register")
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(data.username, data.clave, data.email, db)