from fastapi import APIRouter

# Importamos el router de email. Asumimos que el archivo se llama email_routes.py
# y contiene una instancia APIRouter llamada 'router'.
from .email_routes import router as email_router
from .access_routes import router as access_router
from .predict_routes import router as predict_routes 
from .clientes_routes import router as clientes_router 
# El 'router' es la instancia que contendrá todas tus rutas generales
router = APIRouter(
    tags=["General"] # Etiqueta para agrupar en la documentación
)

# Incluimos las rutas específicas de email. 
# Esto hará que todas las rutas de email_router (como /draft y /send) 
# sean accesibles bajo el prefijo /email.
router.include_router(email_router, prefix="/email")
router.include_router(access_router)
router.include_router(predict_routes, prefix="/predict")
router.include_router(clientes_router, prefix="/clientes")
# -------------------------------------------------------------
# Rutas Generales
# -------------------------------------------------------------

@router.get("/")
async def home_page():
    """Ruta de bienvenida principal."""
    return {"message": "Bienvenido al Backend del Sistema de Scoring."}



@router.get("/abm-productos")
async def abm_productos_page():
    """Ruta para la gestión de productos (ABM)."""
    return {"message": "<h1>Gestión de Productos (ABM)</h1><p>Aquí se gestionarán los productos.</p>"}
