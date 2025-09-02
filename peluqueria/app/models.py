from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.database import Base


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, index=True)

    # El mascota_id y cliente_id se refieren a IDs de otros servicios.
    # La consistencia de los datos se mantiene a nivel de aplicación.
    mascota_id = Column(Integer, index=True, nullable=False)
    cliente_id = Column(Integer, index=True, nullable=False)

    peluquero_id = Column(Integer, ForeignKey("peluqueros.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))

    peluquero = relationship("Peluquero")
    servicio = relationship("Servicio")


class Peluquero(Base):
    __tablename__ = "peluqueros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    # El user_id lo vincularía a un usuario del servicio de autenticación
    # con el rol 'peluquero'.
    user_id = Column(Integer, unique=True)


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(
        String, unique=True, nullable=False
    )  # Ej: "Baño y Corte", "Corte de Uñas"
    descripcion = Column(String)
    duracion_minutos = Column(Integer)
    precio = Column(Integer)
