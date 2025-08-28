from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Tienda (Pet Shop)",
    description="Microservicio para gestionar inventario, productos, proveedores y punto de venta.",
    version="0.1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/productos/", response_model=List[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de productos con su stock actual.
    """
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.post("/productos/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto en el inventario.
    """
    return crud.create_producto(db=db, producto=producto)

@app.post("/upload-inventario/")
async def upload_inventario(file: UploadFile = File(...)):
    """
    Endpoint para cargar y procesar un archivo (ej. Excel) para actualizar el inventario.
    Para archivos grandes, esto debería ser una tarea asíncrona (Celery + Redis)
    para no bloquear el servidor. El archivo se guarda y se encola una tarea
    para su procesamiento en segundo plano.
    """
    # Placeholder para la lógica de procesamiento de archivos
    # 1. Guardar el archivo temporalmente.
    # 2. Llamar a una tarea de Celery pasándole la ruta del archivo.
    # 3. La tarea de Celery usaría pandas para leer el Excel y actualizar la DB.
    return {"filename": file.filename, "status": "Archivo recibido, pendiente de procesamiento."}

@app.post("/pos/venta/")
def registrar_venta(venta: schemas.Venta, db: Session = Depends(get_db)):
    """
    Endpoint de Punto de Venta (TPV).
    Recibe una lista de productos y cantidades, y actualiza el stock.
    """
    # Lógica para procesar la venta y descontar el stock
    for item in venta.items:
        crud.update_stock_producto(db, producto_id=item.producto_id, cantidad_vendida=item.cantidad)

    db.commit()
    return {"status": "Venta registrada y stock actualizado."}

@app.get("/")
def read_root():
    return {"service": "Petshop Service"}
