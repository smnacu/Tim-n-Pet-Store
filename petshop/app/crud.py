from sqlalchemy.orm import Session
from . import models, schemas

def get_producto(db: Session, producto_id: int):
    """
    Obtiene un producto por su ID.
    """
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de todos los productos.
    """
    return db.query(models.Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: schemas.ProductoCreate):
    """
    Crea un nuevo producto.
    """
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_stock_producto(db: Session, producto_id: int, cantidad_vendida: int):
    """
    Actualiza el stock de un producto.
    Esta función es clave para el TPV.
    """
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db_producto.stock -= cantidad_vendida
        # Aquí se podría añadir lógica para manejar stock negativo o alertas de bajo stock.
        # db.add(db_producto)
        # db.commit()
        # db.refresh(db_producto)
    return db_producto

# Aquí irían las funciones CRUD para Proveedores.
# Ejemplo: create_proveedor, get_proveedores, etc.
