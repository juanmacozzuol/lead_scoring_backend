from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session   
from sqlalchemy import text          
from app.database import get_db      

# 1. Instancia de la aplicación FastAPI
app = FastAPI()

# 2. Definición de una ruta (endpoint) usando un decorador
@app.get("/")
def read_root():
    # 3. La función de ruta devuelve el dato que se convertirá a JSON
    return {"Hello": "World"}

# Otro ejemplo de ruta con un parámetro de path
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


#prueba de conexion a la DB
@app.get("/probandoDB")
def ping_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "ok"}
    except Exception as e:
        return {"db_status": "error", "detail": str(e)}