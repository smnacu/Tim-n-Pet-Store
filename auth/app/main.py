from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from common.database import SessionLocal, engine

# Crear las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

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

@app.post("/token")
def login_for_access_token():
    """
    Endpoint para el login de usuarios.
    Devuelve un token JWT que se usará para autenticar las peticiones
    a otros microservicios.
    La lógica de autenticación (verificación de contraseña y generación de token)
    debe ser implementada aquí.
    """
    # Placeholder para la lógica de login
    return {"message": "Login endpoint - Implementar lógica de JWT"}

@app.get("/")
def read_root():
    return {"service": "Auth Service"}
