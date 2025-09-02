from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from common.database import SessionLocal, engine

from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Tienda (Pet Shop)",
    description=(
        "Microservicio para gestionar inventario, productos, "
        "proveedores y punto de venta."
    ),
    version="0.1.0",
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


@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por ID.
    """
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_producto


@app.post("/proveedores/", response_model=schemas.Proveedor)
def create_proveedor(proveedor: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo proveedor.
    """
    db_proveedor = crud.get_proveedor_by_name(db, name=proveedor.nombre)
    if db_proveedor:
        raise HTTPException(status_code=400, detail="Proveedor already exists")
    return crud.create_proveedor(db=db, proveedor=proveedor)


@app.get("/proveedores/", response_model=List[schemas.Proveedor])
def read_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene lista de proveedores.
    """
    return crud.get_proveedores(db, skip=skip, limit=limit)


@app.post("/categorias/", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría.
    """
    db_categoria = crud.get_categoria_by_name(db, name=categoria.nombre)
    if db_categoria:
        raise HTTPException(status_code=400, detail="Categoria already exists")
    return crud.create_categoria(db=db, categoria=categoria)


@app.get("/categorias/", response_model=List[schemas.Categoria])
def read_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene lista de categorías.
    """
    return crud.get_categorias(db, skip=skip, limit=limit)


@app.get("/categorias/{categoria_id}/productos/", response_model=List[schemas.Producto])
def read_productos_by_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Obtiene productos por categoría.
    """
    return crud.get_productos_by_categoria(db, categoria_id=categoria_id)


@app.post("/upload-inventario/")
async def upload_inventario(file: UploadFile = File(...)):
    """
    Endpoint para cargar y procesar un archivo (ej. Excel) para actualizar
    el inventario. Usa Celery + Redis para procesamiento asíncrono.
    """
    try:
        # Importar la tarea de Celery
        from .tasks import process_inventory_file

        # Simular guardado del archivo
        file_path = f"/tmp/{file.filename}"
        file_type = "excel" if file.filename.endswith((".xlsx", ".xls")) else "csv"

        # Encolar la tarea de procesamiento
        task = process_inventory_file.delay(file_path, file_type)

        return {
            "filename": file.filename,
            "task_id": task.id,
            "status": "Archivo recibido y encolado para procesamiento",
            "file_type": file_type,
        }
    except Exception as e:
        return {
            "filename": file.filename,
            "status": "Error al procesar archivo",
            "error": str(e),
        }


@app.get("/inventario/task/{task_id}")
async def get_inventory_task_status(task_id: str):
    """
    Obtiene el estado de una tarea de procesamiento de inventario.
    """
    try:
        from common.celery_app import celery_app

        # Obtener el resultado de la tarea
        result = celery_app.AsyncResult(task_id)

        if result.ready():
            if result.successful():
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "result": result.result,
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "error": str(result.result),
                }
        else:
            return {"task_id": task_id, "status": "processing"}
    except Exception as e:
        return {"task_id": task_id, "status": "error", "error": str(e)}


@app.post("/reportes/inventario/")
async def generate_inventory_report_endpoint(
    store_id: int = 1, report_type: str = "stock_low"
):
    """
    Genera reportes de inventario de forma asíncrona.
    """
    try:
        from .tasks import generate_inventory_report

        # Encolar la tarea de generación de reporte
        task = generate_inventory_report.delay(store_id, report_type)

        return {
            "message": "Generación de reporte iniciada",
            "task_id": task.id,
            "store_id": store_id,
            "report_type": report_type,
            "status": "processing",
        }
    except Exception as e:
        return {
            "message": "Error al generar reporte",
            "error": str(e),
            "status": "error",
        }


@app.post("/pos/venta/")
def registrar_venta(venta: schemas.Venta, db: Session = Depends(get_db)):
    """
    Endpoint de Punto de Venta (TPV).
    Recibe una lista de productos y cantidades, y actualiza el stock.
    """
    try:
        # Procesar cada item de la venta
        for item in venta.items:
            crud.update_stock_producto(
                db, producto_id=item.producto_id, cantidad_vendida=item.cantidad
            )

        db.commit()
        return {"status": "Venta registrada y stock actualizado exitosamente."}

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )


@app.get("/")
def read_root():
    return {"service": "Petshop Service"}
