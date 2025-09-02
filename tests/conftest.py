"""
Configuración base para tests de integración.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from common.database import Base

# Configuración de base de datos de prueba
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

# Crear motor de prueba
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Crear sesión de prueba
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def setup_test_db():
    """Configurar base de datos de prueba."""
    # Configurar variable de entorno para evitar errores
    os.environ["DATABASE_URL"] = TEST_SQLALCHEMY_DATABASE_URL
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)
    yield
    # Limpiar después de los tests
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_db_session(setup_test_db):
    """Proporcionar sesión de base de datos para tests."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


def override_get_db():
    """Override para la dependencia de base de datos en tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()