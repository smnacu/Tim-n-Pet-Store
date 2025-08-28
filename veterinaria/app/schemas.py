from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# --- Esquemas para Documento ---
class DocumentoBase(BaseModel):
    nombre_archivo: str
    url_archivo: str
    tipo_documento: str

class DocumentoCreate(DocumentoBase):
    pass

class Documento(DocumentoBase):
    id: int
    historial_id: int

    class Config:
        orm_mode = True

# --- Esquemas para Consulta ---
class ConsultaBase(BaseModel):
    fecha: date
    motivo: str
    diagnostico: str
    tratamiento: str

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id: int
    historial_id: int

    class Config:
        orm_mode = True

# --- Esquemas para Historial Clínico ---
class HistorialClinicoBase(BaseModel):
    pass

class HistorialClinicoCreate(HistorialClinicoBase):
    pass

class HistorialClinico(HistorialClinicoBase):
    id: int
    mascota_id: int
    consultas: List[Consulta] = []
    documentos: List[Documento] = []

    class Config:
        orm_mode = True

# --- Esquemas para Mascota ---
class MascotaBase(BaseModel):
    nombre: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    propietario_id: int

class MascotaCreate(MascotaBase):
    pass

class Mascota(MascotaBase):
    id: int
    historial_clinico: Optional[HistorialClinico] = None

    class Config:
        orm_mode = True
