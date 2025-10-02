# routers/app_routes.py

from fastapi import APIRouter

# El 'router' es la instancia que contendrá todas tus rutas
router = APIRouter()

@router.get("/")
async def home_page():
    return {"message": "Bienvenido al Backend del Sistema de Scoring."}

@router.get("/login")
async def login_page():
    return {"message": "<h1>Página de Login</h1><p>Esta es la página para iniciar sesión.</p>"}

@router.get("/register")
async def register_page():
    return {"message": "<h1>Página de Registro</h1><p>Aquí los usuarios pueden registrarse.</p>"}

@router.get("/enviar-mail")
async def enviar_mail_page():
    return {"message": "<h1>Página para Enviar Mails</h1><p>Desde aquí se enviarán correos personalizados.</p>"}

@router.get("/mails-enviados")
async def mails_enviados_page():
    return {"message": "<h1>Página de Mails Enviados</h1><p>Aquí se verá el registro de correos enviados.</p>"}

@router.get("/abm-productos")
async def abm_productos_page():
    return {"message": "<h1>Gestión de Productos (ABM)</h1><p>Aquí se gestionarán los productos.</p>"}