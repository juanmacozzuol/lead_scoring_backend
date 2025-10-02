from fastapi import APIRouter

# Importamos el router de email. Asumimos que el archivo se llama email_routes.py
# y contiene una instancia APIRouter llamada 'router'.
from .email_routes import router as email_router

# El 'router' es la instancia que contendrá todas tus rutas generales
router = APIRouter(
    tags=["General"] # Etiqueta para agrupar en la documentación
)

# Incluimos las rutas específicas de email. 
# Esto hará que todas las rutas de email_router (como /draft y /send) 
# sean accesibles bajo el prefijo /email.
router.include_router(email_router, prefix="/email")

# -------------------------------------------------------------
# Rutas Generales
# -------------------------------------------------------------

@router.get("/")
async def home_page():
    """Ruta de bienvenida principal."""
    return {"message": "Bienvenido al Backend del Sistema de Scoring."}

@router.get("/login")
async def login_page():
    """Ruta de login."""
    return {"message": "<h1>Página de Login</h1><p>Esta es la página para iniciar sesión.</p>"}

@router.get("/register")
async def register_page():
    """Ruta de registro de usuarios."""
    return {"message": "<h1>Página de Registro</h1><p>Aquí los usuarios pueden registrarse.</p>"}

@router.get("/abm-productos")
async def abm_productos_page():
    """Ruta para la gestión de productos (ABM)."""
    return {"message": "<h1>Gestión de Productos (ABM)</h1><p>Aquí se gestionarán los productos.</p>"}
