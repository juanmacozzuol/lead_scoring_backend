from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session   
from sqlalchemy import text          
from .database.database import get_db      
from app.routers import routes


# 1. Instancia de la aplicación FastAPI 
app = FastAPI()

# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(routes.router)
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
    

    