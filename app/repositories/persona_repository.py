from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_persona_por_dni(db: Session, dni: str):
    """
    Obtiene una persona de la base de datos por su DNI.
    Retorna el objeto Row o None si no existe.
    """
    query = text("SELECT * FROM personas WHERE dni = :dni")
    return db.execute(query, {"dni": dni}).fetchone()


def obtener_provincia_por_persona(db: Session, id_persona: int):
    """
    Devuelve la provincia asociada a una persona, si tiene dirección cargada.
    """
    query = text("""
        SELECT provincia FROM direccion 
        WHERE id_persona = :id_persona
        LIMIT 1
    """)

    return db.execute(query, {"id_persona": id_persona}).scalar()

def get_all_clients(db: Session):
    """
    Devuelve todas las personas junto con sus productos asociados.
    """
    query = text("""
        SELECT 
            p.id_persona,
            CONCAT(p.nombre, ' ', p.apellido) AS nombre_completo,
            p.dni,
            GROUP_CONCAT(prod.tipo_producto SEPARATOR ', ') AS productos
        FROM personas p
        LEFT JOIN polizas po ON p.id_persona = po.id_persona
        LEFT JOIN productos prod ON po.id_producto = prod.id_producto
        GROUP BY p.id_persona, p.nombre, p.apellido, p.dni
        ORDER BY p.nombre ASC;
    """)

    result = db.execute(query).fetchall()

    clients = []
    for row in result:
        data = row._mapping
        clients.append({
            "id_persona": data["id_persona"],
            "nombre": data["nombre_completo"],  # 👈 usamos el nombre concatenado
            "dni": data["dni"],
            "productos": data["productos"].split(", ") if data["productos"] else []
        })

    return clients