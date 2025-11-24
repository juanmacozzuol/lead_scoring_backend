import os
from dotenv import load_dotenv
import json
from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import brevo_python
from brevo_python.models.send_smtp_email import SendSmtpEmail
import re
import bleach

# Cargar variables desde .env
load_dotenv()

# Importar modelos de la BD
from app.models.user_db_models import (
    Persona,
    Usuario
)
from app.models.email_db_models import (
    Correo
)

from app.models.insurance_db_models import (
    Producto
)


# Importar modelos Pydantic
from app.models.email_models import (
    GenerarBorradorRequest, 
    EnviarCorreoRequest,
    EnviarCorreoResponse,
    CorreoGuardadoCreate,
    CorreoGuardadoUpdate
)

from app.services import llm_service

# Configuracion del Servicio
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@bdt-seguros.com")
COMPANY_NAME = os.getenv("COMPANY_NAME", "BDT Seguros")

# Para la limpieza de respuesta LLM
TAGS_PERMITIDOS = [
    'p', 'br', 'strong', 'em', 'u', 'b', 'i',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'span', 'div'
]

ATRIBUTOS_PERMITIDOS = {
    'a': ['href', 'title', 'target'],
    'p': ['style'],
    'div': ['style'],
    'span': ['style'],
    'h1': ['style'], 'h2': ['style'], 'h3': ['style'],
    'strong': ['style'], 'em': ['style']
}


# Helpers

def _calcular_edad(fecha_nacimiento: date) -> int:
    """Helper para calcular la edad."""
    hoy = datetime.utcnow().date()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# IMPORTANTE:
# Si el dia de mañana quieren usar otro proveedor (como Mailgun o SendGrid), el unico cambio que se deberia hacer con esta estructura es:
# Crear una nueva funcion privada en este archivo email_service.py (ej. _enviar_por_mailgun(...)) con la logica necesaria de ese nuevo proveedor.
# Ir a la funcion enviar_correo_adhoc.
# Reemplazar la linea _enviar_por_brevo(...) por la nueva _enviar_por_mailgun(...).

def _enviar_por_brevo(to_email: str, subject: str, body_html: str):
    """Funcion aislada para enviar el email via Brevo."""
    
    # Configuracion el cliente de Brevo
    configuracion = brevo_python.Configuration()
    # Lee la API key. Asegurate de agregarla a tu .env
    configuracion.api_key['api-key'] = BREVO_API_KEY
    
    if not configuracion.api_key['api-key']:
        raise HTTPException(status_code=503, detail="BREVO_API_KEY no esta configurada en el servidor")

    api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuracion))
    
    # Se crea el objeto del email
    send_smtp_email = SendSmtpEmail(
        to=[{"email": to_email}],
        html_content=body_html,
        subject=subject,
        sender={"email": FROM_EMAIL, "name": COMPANY_NAME} # Se debe asegurar que FROM_EMAIL sea un email verificado en Brevo
    )
    
    # Enviar
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Respuesta de Brevo: {api_response}") # Log para saber que funciono
    except Exception as e:
        # Relanzamos la excepcion para que la funcion principal la atrape
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar el correo con Brevo: {str(e)}"
        )

def _registrar_correo_enviado(db: Session, req: EnviarCorreoRequest, id_usuario: int, exito: bool) -> Correo:
    """Guarda el resultado del envio en la tabla Correo (auditoria)."""
    
    # Usamos .date() para que coincida con el tipo 'Date' de nuestra estructura
    fecha_actual = datetime.utcnow().date()
    
    log_entry = Correo(
        asunto=req.asunto,
        cuerpo=req.cuerpo,
        fecha_creacion=fecha_actual,
        fecha_envio=fecha_actual if exito else None,
        id_persona=req.id_persona,
        id_producto=req.id_producto,
        id_usuario=id_usuario
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


# Generacion y envio

def generar_borrador_ia(db: Session, req: GenerarBorradorRequest):
    """
    Funcion principal para generar un borrador con el motor LLM.
    """
    
    # Obtenemos datos de la BD
    persona = db.query(Persona).filter(Persona.id_persona == req.id_persona).first()
    producto = db.query(Producto).filter(Producto.id_producto == req.id_producto).first()
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    # Mejormaos datos
    edad = _calcular_edad(persona.fecha_nacimiento)
    ciudad = persona.direcciones[0].ciudad if persona.direcciones else "Ciudad desconocida"

    # Construccion del PROMPT
    prompt = f"""
        Eres un asistente de ventas experto de la compañía de seguros "{COMPANY_NAME}".
        Debes redactar un email personalizado para promocionar un producto.

        DATOS DEL CLIENTE:
        - Nombre: {persona.nombre}
        - Edad: {edad} años
        - Ciudad: {ciudad}
        - Ocupación: {persona.ocupacion or "No especificada"}
        - Estado Civil: {persona.estado_civil}
        - Hijos: {persona.cantidad_hijos}
        - Vivienda Propia: {"Sí" if persona.vivienda_propia else "No"}
        - Auto: {"Sí" if persona.posee_auto else "No"}

        DATOS DEL PRODUCTO:
        - Nombre: {producto.nombre}
        - Tipo: {producto.tipo_producto}
        - Coberturas: {producto.coberturas_incluidas}
        - Prima Base: ${producto.prima_base}

        CONTEXTO DE LA RELACIÓN:
        - Etapa: {req.etapa_relacion}
        * "prospecto": Primera vez que contactamos al cliente
        * "cliente_activo": Ya tiene pólizas con nosotros
        * "cliente_inactivo": Tuvo pólizas pero ya no está activo

        TONO REQUERIDO: {req.formalidad}
        - "muy_formal": Tratamiento de usted, lenguaje corporativo
        - "neutral": Equilibrio entre profesional y cercano
        - "informal": Tratamiento de tú, lenguaje conversacional

        INSTRUCCIONES CRÍTICAS:
        1. USA los datos para inferir necesidades, pero NO los menciones explícitamente como datos crudos. 
           (Ejemplo: Si tiene hijos, habla de "proteger el futuro de tu familia", NO digas "como tienes 2 hijos").
           (Ejemplo: Si tiene 50 años, habla de "tranquilidad y respaldo", NO digas "a tus 50 años").
        2. Máximo 3 párrafos.
        3. Incluye un llamado a la acción claro.
        4. NO inventes datos que no te di.
        5. NO uses saludo genérico "Estimado Cliente" - usa su nombre.
        6. Adapta el mensaje a la etapa de relación.
        7. PROHIBIDO mencionar la edad exacta, estado civil o cantidad numérica de hijos en el texto. Úsalos solo para deducir el "pain point" (punto de dolor) del cliente.

        FORMATO DE SALIDA (OBLIGATORIO):
        Debes devolver ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
        {{
        "asunto_sugerido": "texto del asunto",
        "cuerpo_sugerido": "texto del email en HTML básico"
        }}

        NO incluyas ningún texto adicional fuera del JSON.
        NO uses markdown code blocks.
        El cuerpo_sugerido debe usar HTML básico: <p>, <strong>, <br>, <ul>, <li>
        """

    
    # Llamada al motor LLM (Google, OpenAI o Local)
    try:
        # Esta funcion decide a que LLM llamar (Google, OpenAI o Local)
        json_string_response = llm_service.generar_json_email(prompt)

        # Intenta extraer el JSON si viene con texto extra
        json_match = re.search(r'\{.*\}', json_string_response, re.DOTALL)
        if json_match:
            draft_json = json.loads(json_match.group())
        else:
        # Parseamos la respuesta JSON del LLM
            draft_json = json.loads(json_string_response)

        # Validar claves
        if "asunto_sugerido" not in draft_json or "cuerpo_sugerido" not in draft_json:
            # En vez de dejar pasar None, devolvemos algo válido con placeholders
            draft_json = {"asunto_sugerido": "Asunto no generado", "cuerpo_sugerido": "<p>No se pudo generar el cuerpo</p>"}

        return draft_json # Devuelve {"asunto_sugerido": "...", "cuerpo_sugerido": "..."}
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, 
            detail="El LLM devolvio una respuesta invalida (no es JSON).")
    except Exception as e:
        # Capturamos errores de la capa LLM (API Keys, timeouts, etc)
        raise HTTPException(
            status_code=500, 
            detail=f"Error generando borrador: {str(e)}")
    

def _limpiar_html(html: str) -> str:
    """Limpia el HTML usando las reglas globales."""
    return bleach.clean(
        html, 
        tags=TAGS_PERMITIDOS, 
        attributes=ATRIBUTOS_PERMITIDOS, 
        strip=True
    )

def _limpiar_asunto(asunto: str) -> str:
    """Elimina TODO el HTML del asunto."""
    return bleach.clean(asunto, tags=[], strip=True)


def enviar_correo_adhoc(db: Session, req: EnviarCorreoRequest, current_user: Usuario) -> EnviarCorreoResponse:
    """
    Envia el email de texto libre (editado por el empleado).
    Esta es ahora la UNICA forma de enviar.
    """
    
    # Validamos que los IDs existan
    persona = db.query(Persona).filter(Persona.id_persona == req.id_persona).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if not persona.email:
        raise HTTPException(status_code=400, detail="La persona no tiene un email registrado")
    if not db.query(Producto).filter(Producto.id_producto == req.id_producto).first():
        raise HTTPException(status_code=404, detail="Producto no encontrado (para log)")

    log_entry = None
    try:
        # Enviamos Email
        cuerpo_limpio = _limpiar_html(req.cuerpo)
        asunto_limpio = _limpiar_asunto(req.asunto)        
        
        _enviar_por_brevo(
            to_email=persona.email,
            subject=asunto_limpio,
            body_html=cuerpo_limpio
        )

        
        # Registramos Auditoria (Exito)
        log_entry = _registrar_correo_enviado(db, req, current_user.id_usuario, exito=True)
        
        return EnviarCorreoResponse(
            status="enviado", 
            mensaje=f"Correo enviado exitosamente a {persona.email}",
            id_correo_log=log_entry.id_correo
        )
    
    except Exception as e:
        # Registramos Auditoria (Fallo)
        # (Solo si el error fue de Brevo, no de validacion)
        if "Error al enviar" in str(e) or "Error de Brevo" in str(e):
             log_entry = _registrar_correo_enviado(db, req, current_user.id_usuario, exito=False)
        
        # Relanzamos la excepcion
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=str(e))