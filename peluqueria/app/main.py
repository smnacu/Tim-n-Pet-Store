from fastapi import FastAPI, Depends
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

@app.get("/")
def read_root():
    return {"service": "Peluqueria Service"}
