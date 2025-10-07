import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables del .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear engine y sesión
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # reintenta si la conexión se cayó
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Dependencia para FastAPI (abre y cierra sesión por request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper opcional: test rápido de conexión (no crea tablas)
def ping():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
