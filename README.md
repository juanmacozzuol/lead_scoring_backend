## Actualización – 18/09/2025

- Se actualizó el archivo `requirements.txt` con las nuevas dependencias. (**SQLAlchemy** y **PyMySQL**.)

### Instrucciones 
1. Hacer `git pull` para traer los cambios más recientes del repo en caso que sea necesario.
2. Instalar las nuevas dependencias:
   
  corer en en terminal el siguiente comando :  pip install -r requirements.txt

## IMPORTANTE ## : 
- Crear en MySQL una base de datos vacía llamada: lead_scoring

- Crear archivo .env  (solicitar por whatsapp)

- Levantar el backend con: python -m uvicorn app.main:app --reload

- Probar la conexión de la db con : 
http://127.0.0.1:8000/probandoDB
Si todo está correcto debería devolver:

{"db_status": "ok"}