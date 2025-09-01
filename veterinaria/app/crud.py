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

# --- CRUD para Consultas ---
def create_consulta(db: Session, consulta: schemas.ConsultaCreate, historial_id: int):
    """
    Crea una nueva consulta asociada a un historial clínico.
    """
    db_consulta = models.Consulta(**consulta.dict(), historial_id=historial_id)
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

def get_consultas_by_historial(db: Session, historial_id: int):
    """
    Obtiene todas las consultas de un historial clínico específico.
    """
    return db.query(models.Consulta).filter(models.Consulta.historial_id == historial_id).all()

# --- CRUD para Documentos ---
def create_documento(db: Session, documento: schemas.DocumentoCreate, historial_id: int):
    """
    Crea un nuevo documento asociado a un historial clínico.
    """
    db_documento = models.Documento(**documento.dict(), historial_id=historial_id)
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def get_documentos_by_historial(db: Session, historial_id: int):
    """
    Obtiene todos los documentos de un historial clínico específico.
    """
    return db.query(models.Documento).filter(models.Documento.historial_id == historial_id).all()

# --- CRUD para Historial Clínico ---
def get_historial_by_mascota(db: Session, mascota_id: int):
    """
    Obtiene el historial clínico de una mascota específica.
    """
    return db.query(models.HistorialClinico).filter(models.HistorialClinico.mascota_id == mascota_id).first()

def get_mascota_by_propietario(db: Session, propietario_id: int):
    """
    Obtiene todas las mascotas de un propietario específico.
    """
    return db.query(models.Mascota).filter(models.Mascota.propietario_id == propietario_id).all()
