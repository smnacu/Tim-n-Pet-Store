from typing import List

from passlib.context import CryptContext
from sqlalchemy.orm import Session

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

    # Asignar roles al usuario
    if user.roles:
        for role_name in user.roles:
            role = get_role_by_name(db, role_name)
            if role:
                db_user.roles.append(role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    """
    Verifica que la contraseña en texto plano coincida con el hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    """
    Autentica un usuario verificando email y contraseña.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# --- CRUD para Roles ---


def create_role(db: Session, role: schemas.RoleCreate):
    """
    Crea un nuevo rol en la base de datos.
    """
    db_role = models.Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role(db: Session, role_id: int):
    """
    Obtiene un rol por su ID.
    """
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    """
    Obtiene un rol por su nombre.
    """
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de roles.
    """
    return db.query(models.Role).offset(skip).limit(limit).all()
