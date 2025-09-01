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


# --- CRUD para Peluqueros ---
def get_peluquero(db: Session, peluquero_id: int):
    """
    Obtiene un peluquero por su ID.
    """
    return (
        db.query(models.Peluquero).filter(models.Peluquero.id == peluquero_id).first()
    )


def get_peluqueros(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de peluqueros.
    """
    return db.query(models.Peluquero).offset(skip).limit(limit).all()


def create_peluquero(db: Session, peluquero: schemas.PeluqueroCreate):
    """
    Crea un nuevo peluquero en la base de datos.
    """
    db_peluquero = models.Peluquero(**peluquero.dict())
    db.add(db_peluquero)
    db.commit()
    db.refresh(db_peluquero)
    return db_peluquero


# --- CRUD para Servicios ---
def get_servicio(db: Session, servicio_id: int):
    """
    Obtiene un servicio por su ID.
    """
    return db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()


def get_servicios(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de servicios.
    """
    return db.query(models.Servicio).offset(skip).limit(limit).all()


def create_servicio(db: Session, servicio: schemas.ServicioCreate):
    """
    Crea un nuevo servicio en la base de datos.
    """
    db_servicio = models.Servicio(**servicio.dict())
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def get_servicio_by_name(db: Session, name: str):
    """
    Obtiene un servicio por su nombre.
    """
    return db.query(models.Servicio).filter(models.Servicio.nombre == name).first()
