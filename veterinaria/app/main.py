from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from common.database import SessionLocal, engine

from . import crud, models, schemas

# Crear tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Veterinaria",
    description="Microservicio para gestionar historiales clínicos, consultas y documentos de mascotas.",
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
def upload_documento():
    """
    Endpoint para subir un documento (radiografía, análisis).
    Aquí se podría integrar una tarea asíncrona (Celery + Redis)
    para procesar el documento, por ejemplo, usando OCR para digitalizar
    historiales en papel.
    """
    # Lógica para guardar el archivo y encolar la tarea de procesamiento
    return {"message": "Documento recibido. Implementar lógica de procesamiento OCR."}


@app.get("/")
def read_root():
    return {"service": "Veterinaria Service"}
