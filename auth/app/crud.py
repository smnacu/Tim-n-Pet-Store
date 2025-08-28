from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas

# Contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    """
    Obtiene un usuario por su ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Obtiene un usuario por su email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de usuarios.
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    Hashea la contraseña antes de guardarla.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    # Aquí se añadiría la lógica para asignar roles
    # Por ejemplo, buscar los roles en la DB y asignarlos al usuario.

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    """
    Verifica que la contraseña en texto plano coincida con el hash.
    """
    return pwd_context.verify(plain_password, hashed_password)
