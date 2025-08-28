from sqlalchemy.orm import Session
from . import models, schemas

def get_turno(db: Session, turno_id: int):
    """
    Obtiene un turno por su ID.
    """
    return db.query(models.Turno).filter(models.Turno.id == turno_id).first()

def get_turnos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de todos los turnos.
    """
    return db.query(models.Turno).offset(skip).limit(limit).all()

def create_turno(db: Session, turno: schemas.TurnoCreate):
    """
    Crea un nuevo turno en la base de datos.
    Aquí se añadiría la lógica de validación de disponibilidad.
    """
    db_turno = models.Turno(**turno.dict())
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno

# Aquí irían las funciones CRUD para Peluqueros y Servicios.
# Ejemplo: create_peluquero, get_servicios, etc.
