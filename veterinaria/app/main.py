from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from common.database import SessionLocal, engine

from . import crud, models, schemas

# Crear tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Veterinaria",
    description=(
        "Microservicio para gestionar historiales clínicos, "
        "consultas y documentos de mascotas."
    ),
    version="0.1.0",
)


# Dependencia de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/mascotas/", response_model=schemas.Mascota)
def create_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva mascota en el sistema.
    """
    return crud.create_mascota(db=db, mascota=mascota)


@app.get("/mascotas/", response_model=List[schemas.Mascota])
def read_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las mascotas.
    """
    mascotas = crud.get_mascotas(db, skip=skip, limit=limit)
    return mascotas


@app.get("/mascotas/{mascota_id}", response_model=schemas.Mascota)
def read_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una mascota específica, incluyendo su historial clínico.
    """
    db_mascota = crud.get_mascota(db, mascota_id=mascota_id)
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota not found")
    return db_mascota


@app.post("/mascotas/{mascota_id}/consultas/", response_model=schemas.Consulta)
def create_consulta(
    mascota_id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)
):
    """
    Crea una nueva consulta para una mascota específica.
    """
    historial = crud.get_historial_by_mascota(db, mascota_id=mascota_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial clínico not found")
    return crud.create_consulta(db=db, consulta=consulta, historial_id=historial.id)


@app.get("/mascotas/{mascota_id}/consultas/", response_model=List[schemas.Consulta])
def read_consultas(mascota_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las consultas de una mascota específica.
    """
    historial = crud.get_historial_by_mascota(db, mascota_id=mascota_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial clínico not found")
    return crud.get_consultas_by_historial(db, historial_id=historial.id)


@app.post("/mascotas/{mascota_id}/documentos/", response_model=schemas.Documento)
def create_documento(
    mascota_id: int, documento: schemas.DocumentoCreate, db: Session = Depends(get_db)
):
    """
    Crea un nuevo documento para una mascota específica.
    """
    historial = crud.get_historial_by_mascota(db, mascota_id=mascota_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial clínico not found")
    return crud.create_documento(db=db, documento=documento, historial_id=historial.id)


@app.get(
    "/propietarios/{propietario_id}/mascotas/", response_model=List[schemas.Mascota]
)
def read_mascotas_by_propietario(propietario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las mascotas de un propietario específico.
    """
    return crud.get_mascota_by_propietario(db, propietario_id=propietario_id)


@app.post("/historias-clinicas/")
async def upload_documento():
    """
    Endpoint para subir un documento (radiografía, análisis).
    Usa Celery + Redis para procesar el documento de forma asíncrona
    con OCR para digitalizar historiales en papel.
    """
    try:
        # Importar la tarea de Celery
        from .tasks import process_medical_document
        
        # Simular información del archivo subido
        file_path = "/tmp/uploaded_document.pdf"
        document_type = "radiografia"
        
        # Encolar la tarea de procesamiento OCR
        task = process_medical_document.delay(file_path, document_type)
        
        return {
            "message": "Documento recibido y encolado para procesamiento OCR",
            "task_id": task.id,
            "status": "processing"
        }
    except Exception as e:
        return {
            "message": "Error al procesar documento",
            "error": str(e),
            "status": "error"
        }


@app.get("/historias-clinicas/task/{task_id}")
async def get_ocr_task_status(task_id: str):
    """
    Obtiene el estado de una tarea de procesamiento OCR.
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
                    "result": result.result
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "error": str(result.result)
                }
        else:
            return {
                "task_id": task_id,
                "status": "processing"
            }
    except Exception as e:
        return {
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }


@app.post("/mascotas/{mascota_id}/reportes/")
async def generate_medical_report_endpoint(mascota_id: int):
    """
    Genera un reporte médico consolidado para una mascota.
    """
    try:
        from .tasks import generate_medical_report
        
        # Simular IDs de consultas
        consultation_ids = [1, 2, 3]
        
        # Encolar la tarea de generación de reporte
        task = generate_medical_report.delay(mascota_id, consultation_ids)
        
        return {
            "message": "Generación de reporte médico iniciada",
            "task_id": task.id,
            "mascota_id": mascota_id,
            "status": "processing"
        }
    except Exception as e:
        return {
            "message": "Error al generar reporte",
            "error": str(e),
            "status": "error"
        }


@app.get("/")
def read_root():
    return {"service": "Veterinaria Service"}
