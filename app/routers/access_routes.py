# app/routers/access_routes.py

from fastapi import APIRouter, Form
from app.controllers.access_controller import login_user, register_user

router = APIRouter(tags=["Access Operations"])


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login route using username and password."""
    return login_user(username, password)


@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    """Registration route."""
    return register_user(username, password)
