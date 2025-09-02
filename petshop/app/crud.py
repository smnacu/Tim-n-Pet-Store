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
        if db_producto.stock < cantidad_vendida:
            raise ValueError(
                f"Stock insuficiente. Stock actual: {db_producto.stock}, cantidad solicitada: {cantidad_vendida}"
            )

        db_producto.stock -= cantidad_vendida
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
    return db_producto


# --- CRUD para Proveedores ---
def get_proveedor(db: Session, proveedor_id: int):
    """
    Obtiene un proveedor por su ID.
    """
    return (
        db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    )


def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de proveedores.
    """
    return db.query(models.Proveedor).offset(skip).limit(limit).all()


def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    """
    Crea un nuevo proveedor.
    """
    db_proveedor = models.Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor


def get_proveedor_by_name(db: Session, name: str):
    """
    Obtiene un proveedor por su nombre.
    """
    return db.query(models.Proveedor).filter(models.Proveedor.nombre == name).first()


# --- CRUD para Categorías ---
def get_categoria(db: Session, categoria_id: int):
    """
    Obtiene una categoría por su ID.
    """
    return (
        db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    )


def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de categorías.
    """
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """
    Crea una nueva categoría.
    """
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def get_categoria_by_name(db: Session, name: str):
    """
    Obtiene una categoría por su nombre.
    """
    return db.query(models.Categoria).filter(models.Categoria.nombre == name).first()


def get_productos_by_categoria(db: Session, categoria_id: int):
    """
    Obtiene productos por categoría.
    """
    return (
        db.query(models.Producto)
        .filter(models.Producto.categoria_id == categoria_id)
        .all()
    )


def get_productos_by_proveedor(db: Session, proveedor_id: int):
    """
    Obtiene productos por proveedor.
    """
    return (
        db.query(models.Producto)
        .filter(models.Producto.proveedor_id == proveedor_id)
        .all()
    )
