from sqlalchemy.orm import Session
from . import models, schemas

def get_mascota(db: Session, mascota_id: int):
    """
    Obtiene una mascota por su ID, incluyendo su historial clínico.
    """
    return db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()

def get_mascotas(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de todas las mascotas.
    """
    return db.query(models.Mascota).offset(skip).limit(limit).all()

def create_mascota(db: Session, mascota: schemas.MascotaCreate):
    """
    Crea una nueva mascota y, automáticamente, su historial clínico asociado.
    """
    db_mascota = models.Mascota(**mascota.dict())
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)

    # Crear el historial clínico asociado a la mascota
    db_historial = models.HistorialClinico(mascota_id=db_mascota.id)
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)

    # Refrescar el objeto mascota para que incluya el historial recién creado
    db.refresh(db_mascota)

    return db_mascota

# Aquí irían las funciones CRUD para Consultas y Documentos
# Ejemplo: create_consulta, create_documento, etc.
