## Actualización – 18/09/2025

- Se actualizó el archivo `requirements.txt` con las nuevas dependencias.

---

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/juanmacozzuol/lead_scoring_backend
cd lead_scoring_backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y solicitar por whatsapp

### 5. Ejecutar servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. Verificar que funciona

Abre en tu navegador: [http://127.0.0.1:8000/probandoDB](http://127.0.0.1:8000/probandoDB)

Deberías ver:
```json
{
  "db_status": "ok",
}
```

---
