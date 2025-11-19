from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database.database import get_db
from app.models.insurance_db_models import Producto

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

class ProductoCreate(BaseModel):
    nombre: str
    tipo_producto: str
    coberturas_incluidas: str
    prima_base: float

    class Config:
        from_attributes = True


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    tipo_producto: str | None = None
    coberturas_incluidas: str | None = None
    prima_base: float | None = None

    class Config:
        from_attributes = True


class ProductoResponse(BaseModel):
    id_producto: int
    nombre: str
    tipo_producto: str | None
    coberturas_incluidas: str | None
    prima_base: float | None

    class Config:
        from_attributes = True


@router.get("", response_model=List[ProductoResponse])
async def get_productos(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos
    """
    try:
        productos = db.query(Producto).all()
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )


@router.get("/{id_producto}", response_model=ProductoResponse)
async def get_producto(id_producto: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por ID
    """
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id_producto} no encontrado"
        )
    
    return producto


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def create_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto
    """
    try:
        # Validar tipo de producto
        tipos_validos = ['Auto', 'Hogar', 'Vida', 'Salud']
        if producto_data.tipo_producto not in tipos_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de producto inválido. Valores permitidos: {tipos_validos}"
            )
        
        # Validar prima base
        if producto_data.prima_base < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La prima base no puede ser negativa"
            )
        
        # Crear el producto
        nuevo_producto = Producto(
            nombre=producto_data.nombre,
            tipo_producto=producto_data.tipo_producto,
            coberturas_incluidas=producto_data.coberturas_incluidas,
            prima_base=producto_data.prima_base
        )
        
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
        
        return nuevo_producto
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )


@router.put("/{id_producto}", response_model=ProductoResponse)
async def update_producto(
    id_producto: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un producto existente
    """
    try:
        # Buscar el producto
        producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {id_producto} no encontrado"
            )
        
        # Actualizar solo los campos proporcionados
        if producto_data.nombre is not None:
            producto.nombre = producto_data.nombre
        
        if producto_data.tipo_producto is not None:
            tipos_validos = ['Auto', 'Hogar', 'Vida', 'Salud']
            if producto_data.tipo_producto not in tipos_validos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tipo de producto inválido. Valores permitidos: {tipos_validos}"
                )
            producto.tipo_producto = producto_data.tipo_producto
        
        if producto_data.coberturas_incluidas is not None:
            producto.coberturas_incluidas = producto_data.coberturas_incluidas
        
        if producto_data.prima_base is not None:
            if producto_data.prima_base < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La prima base no puede ser negativa"
                )
            producto.prima_base = producto_data.prima_base
        
        db.commit()
        db.refresh(producto)
        
        return producto
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}"
        )


@router.delete("/{id_producto}", status_code=status.HTTP_200_OK)
async def delete_producto(id_producto: int, db: Session = Depends(get_db)):
    """
    Elimina un producto por ID
    NOTA: Solo se puede eliminar si no tiene pólizas asociadas
    """
    try:
        # Buscar el producto
        producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {id_producto} no encontrado"
            )
        
        # Verificar si tiene pólizas asociadas
        if producto.polizas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el producto. Tiene {len(producto.polizas)} pólizas asociadas"
            )
        
        # Verificar si tiene correos asociados
        if producto.correos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el producto. Tiene {len(producto.correos)} correos asociados"
            )
        
        # Eliminar el producto
        db.delete(producto)
        db.commit()
        
        return {"mensaje": f"Producto '{producto.nombre}' eliminado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}"
        )


@router.get("/tipo/{tipo_producto}", response_model=List[ProductoResponse])
async def get_productos_por_tipo(tipo_producto: str, db: Session = Depends(get_db)):
    """
    Obtiene productos filtrados por tipo
    """
    try:
        productos = db.query(Producto).filter(
            Producto.tipo_producto == tipo_producto
        ).all()
        
        return productos
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )