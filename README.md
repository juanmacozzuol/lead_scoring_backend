# Lead Scoring Backend

Backend del proyecto **Lead Scoring**, desarrollado con **FastAPI**, **SQLAlchemy** y **Alembic**.

---

##  Instalación y ejecución local

### 1 Clonar el repositorio
```bash
git clone https://github.com/juanmacozzuol/lead_scoring_backend
cd lead_scoring_backend
```

---

### 2 Crear entorno virtual
```bash
python -m venv venv

# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

---

### 3 Instalar dependencias
```bash
pip install -r requirements.txt
```

---

### 4 Configurar variables de entorno
Crea un archivo **`.env`** en la raíz del proyecto con el siguiente contenido:

```env
DATABASE_URL=
```


> El archivo `.env` se compartirá por privado en caso de requerir credenciales distintas.

---

###  5 Crear la base de datos
Abrí tu cliente de MySQL (por ejemplo desde terminal, Workbench o phpMyAdmin) y ejecutá:

```sql
CREATE DATABASE lead_scoring CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### 6️ Aplicar migraciones Alembic
Alembic se encarga de crear automáticamente todas las tablas definidas en los modelos del proyecto.

```bash
alembic upgrade head
```

 Esto genera la estructura de tablas en la base de datos.

---

### 7️ Ejecutar el seed (datos iniciales)
El seed inserta registros de prueba para validar la API.

```bash
python -m app.database.seeds
```


---

### 8️⃣ Ejecutar el servidor de desarrollo
```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 9️⃣ Verificar conexión a la base de datos
Abrí en tu navegador o en Postman:  
👉 [http://127.0.0.1:8000/probandoDB](http://127.0.0.1:8000/probandoDB)

Deberías obtener:

```json
{
  "db_status": "ok"
}
```

Esto confirma que la base de datos y la API están funcionando correctamente ✅

---

## 🧰 Notas útiles

- Si aparece el error:
  ```
  Target database is not up to date
  ```
  ejecutá:
  ```bash
  alembic downgrade base
  alembic upgrade head
  ```

- Si querés reiniciar todo desde cero:
  ```sql
  DROP DATABASE lead_scoring;
  CREATE DATABASE lead_scoring CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
  Luego volvé a ejecutar:
  ```bash
  alembic upgrade head
  python -m app.database.seeds
  ```

---

## 👩‍💻 Autores
Equipo de Backend del proyectoLead Scoring 
- Ángeles Mendoza  
- Juan Manuel Cozzuol  
- Julian Espinoza
