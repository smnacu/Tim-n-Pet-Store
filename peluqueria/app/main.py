from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from common.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Peluquería Canina",
    description="Microservicio para agendar y gestionar turnos de peluquería.",
    version="0.1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/turnos/", response_model=schemas.Turno)
def create_turno(turno: schemas.TurnoCreate, db: Session = Depends(get_db)):
    """
    Agenda un nuevo turno para un servicio de peluquería.
    La lógica de disponibilidad de peluqueros y cabinas se implementaría aquí.
    """
    return crud.create_turno(db=db, turno=turno)

@app.get("/turnos/", response_model=List[schemas.Turno])
def read_turnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los turnos agendados.
    """
    turnos = crud.get_turnos(db, skip=skip, limit=limit)
    return turnos

@app.get("/turnos/{turno_id}", response_model=schemas.Turno)
def read_turno(turno_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un turno específico por ID.
    """
    db_turno = crud.get_turno(db, turno_id=turno_id)
    if db_turno is None:
        raise HTTPException(status_code=404, detail="Turno not found")
    return db_turno

@app.post("/peluqueros/", response_model=schemas.Peluquero)
def create_peluquero(peluquero: schemas.PeluqueroCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo peluquero en el sistema.
    """
    return crud.create_peluquero(db=db, peluquero=peluquero)

@app.get("/peluqueros/", response_model=List[schemas.Peluquero])
def read_peluqueros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de peluqueros disponibles.
    """
    return crud.get_peluqueros(db, skip=skip, limit=limit)

@app.post("/servicios/", response_model=schemas.Servicio)
def create_servicio(servicio: schemas.ServicioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo servicio de peluquería.
    """
    db_servicio = crud.get_servicio_by_name(db, name=servicio.nombre)
    if db_servicio:
        raise HTTPException(status_code=400, detail="Service already exists")
    return crud.create_servicio(db=db, servicio=servicio)

@app.get("/servicios/", response_model=List[schemas.Servicio])
def read_servicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de servicios disponibles.
    """
    return crud.get_servicios(db, skip=skip, limit=limit)

@app.get("/")
def read_root():
    return {"service": "Peluqueria Service"}
