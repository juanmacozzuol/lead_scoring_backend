from fastapi import FastAPI

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