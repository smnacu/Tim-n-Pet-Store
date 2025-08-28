import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usar la variable de entorno de docker-compose
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/veterinaria_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Comentario sobre Multi-Tenancy ---
# Para un futuro modelo multi-inquilino, se podría modificar la conexión
# para que seleccione un esquema de PostgreSQL específico basado en el tenant (franquicia).
# Esto se podría manejar con un middleware en FastAPI que intercepte la petición,
# identifique al tenant (ej. a través de un subdominio o un header) y configure
# la sesión de la base de datos para usar el esquema correspondiente.
# Ejemplo:
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-csearch_path={}".format(tenant_schema)})
