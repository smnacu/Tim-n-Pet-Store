from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    raza = Column(String)
    sexo = Column(String)
    fecha_nacimiento = Column(Date)

    # El propietario_id vincula la mascota a un usuario del servicio de autenticación.
    # La validación de que este ID existe se haría a nivel de API Gateway o en el frontend.
    propietario_id = Column(Integer, index=True, nullable=False)

    # Relación uno a uno con HistorialClinico
    historial_clinico = relationship("HistorialClinico", back_populates="mascota", uselist=False)

class HistorialClinico(Base):
    __tablename__ = "historiales_clinicos"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))

    # Relación inversa con Mascota
    mascota = relationship("Mascota", back_populates="historial_clinico")

    # Relación uno a muchos con Consultas y Documentos
    consultas = relationship("Consulta", back_populates="historial")
    documentos = relationship("Documento", back_populates="historial")

class Consulta(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    motivo = Column(String)
    diagnostico = Column(Text)
    tratamiento = Column(Text)
    historial_id = Column(Integer, ForeignKey("historiales_clinicos.id"))

    historial = relationship("HistorialClinico", back_populates="consultas")

class Documento(Base):
    __tablename__ = "documentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String)
    url_archivo = Column(String) # URL a un S3 bucket o similar
    tipo_documento = Column(String) # Ej: "Radiografía", "Análisis de Sangre"
    historial_id = Column(Integer, ForeignKey("historiales_clinicos.id"))

    historial = relationship("HistorialClinico", back_populates="documentos")
