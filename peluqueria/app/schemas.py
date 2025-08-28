from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Esquemas para Servicio ---
class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    duracion_minutos: int
    precio: float

class ServicioCreate(ServicioBase):
    pass

class Servicio(ServicioBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Peluquero ---
class PeluqueroBase(BaseModel):
    nombre: str
    user_id: int

class PeluqueroCreate(PeluqueroBase):
    pass

class Peluquero(PeluqueroBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Turno ---
class TurnoBase(BaseModel):
    fecha_hora: datetime
    mascota_id: int
    cliente_id: int
    peluquero_id: int
    servicio_id: int

class TurnoCreate(TurnoBase):
    pass

class Turno(TurnoBase):
    id: int
    peluquero: Peluquero
    servicio: Servicio

    class Config:
        orm_mode = True
