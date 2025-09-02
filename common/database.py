import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Leer la URL de la base de datos desde las variables de entorno.
# La URL debe incluir el search_path para el esquema correcto.
# Ejemplo: postgresql://user:password@postgresql/timon_petstore?options=-csearch_path%3Dusers,public
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise Exception("DATABASE_URL environment variable is not set.")

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una clase de sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos de SQLAlchemy.
# Los modelos que hereden de esta Base usarán el esquema
# definido en el search_path de la DATABASE_URL.
Base = declarative_base()
