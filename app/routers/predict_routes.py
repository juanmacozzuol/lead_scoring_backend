from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.predict_controller import obtener_prediccion_por_dni

router = APIRouter(tags=["Predict"])

@router.get("/{dni}")
def predecir_cliente(dni: str, db: Session = Depends(get_db)):
    """
    Endpoint que recibe un DNI, obtiene los datos del cliente de la base
    y devuelve el score + recomendación de producto.
    """
    resultado = obtener_prediccion_por_dni(dni, db)
    return resultado
