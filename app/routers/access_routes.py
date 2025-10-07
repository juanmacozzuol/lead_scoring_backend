from fastapi import APIRouter


# El 'router' es la instancia que contiene todas tus rutas.
router = APIRouter(
    tags=["Access Operations"]
)

@router.get("/login")
async def login_page():
    """Ruta de login."""
    return {"message": "<h1>Página de Login</h1><p>Esta es la página para iniciar sesión.</p>"}

@router.get("/register")
async def register_page():
    """Ruta de registro de usuarios."""
    return {"message": "<h1>Página de Registro</h1><p>Aquí los usuarios pueden registrarse.</p>"}