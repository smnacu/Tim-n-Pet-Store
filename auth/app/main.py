from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from . import crud, models, schemas, auth_utils
from common.database import SessionLocal, engine

# Crear las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Servicio de Autenticación",
    description="Microservicio para gestionar usuarios, roles y autenticación (JWT).",
    version="0.1.0"
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario.
    Los roles (veterinario, peluquero, admin, cliente) se asignarán aquí.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para el login de usuarios.
    Devuelve un token JWT que se usará para autenticar las peticiones
    a otros microservicios.
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={
            "sub": user.email,
            "roles": [role.name for role in user.roles]
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"service": "Auth Service"}

@app.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rol en el sistema.
    """
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db=db, role=role)

@app.get("/roles/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene lista de roles disponibles.
    """
    return crud.get_roles(db, skip=skip, limit=limit)

@app.get("/users/me", response_model=schemas.User)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene información del usuario actual basada en el token JWT.
    """
    email = auth_utils.verify_token(token)
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene lista de usuarios (requiere autenticación).
    """
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/verify-token")
def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para que otros microservicios verifiquen tokens JWT.
    """
    email = auth_utils.verify_token(token)
    roles = auth_utils.get_user_roles_from_token(token)
    return {"email": email, "roles": roles, "valid": True}
