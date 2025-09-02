"""
Tests de integración para verificar la comunicación entre servicios.
"""

from fastapi.testclient import TestClient

from auth.app.main import app as auth_app, get_db as auth_get_db
from veterinaria.app.main import app as vet_app, get_db as vet_get_db
from petshop.app.main import app as petshop_app, get_db as petshop_get_db
from tests.conftest import override_get_db


# Override de dependencias para tests
auth_app.dependency_overrides[auth_get_db] = override_get_db
vet_app.dependency_overrides[vet_get_db] = override_get_db
petshop_app.dependency_overrides[petshop_get_db] = override_get_db

auth_client = TestClient(auth_app)
vet_client = TestClient(vet_app)
petshop_client = TestClient(petshop_app)


class TestServiceIntegration:
    """Tests de integración entre servicios."""

    def test_auth_service_connectivity(self, setup_test_db):
        """Test que el servicio de auth está funcionando."""
        response = auth_client.get("/")
        assert response.status_code == 200
        assert response.json()["service"] == "Auth Service"

    def test_veterinaria_service_connectivity(self, setup_test_db):
        """Test que el servicio de veterinaria está funcionando."""
        response = vet_client.get("/")
        assert response.status_code == 200
        assert response.json()["service"] == "Veterinaria Service"

    def test_petshop_service_connectivity(self, setup_test_db):
        """Test que el servicio de petshop está funcionando."""
        response = petshop_client.get("/")
        assert response.status_code == 200
        assert response.json()["service"] == "Petshop Service"


class TestCeleryIntegration:
    """Tests de integración para Celery y tareas asíncronas."""

    def test_veterinaria_ocr_endpoint_response(self, setup_test_db):
        """Test que el endpoint de OCR responde correctamente."""
        # Hacer request al endpoint (sin Celery real)
        response = vet_client.post("/historias-clinicas/")

        assert response.status_code == 200
        data = response.json()
        # El endpoint debe responder, aunque sea con error por falta de Celery
        assert "status" in data
        assert data["status"] in ["processing", "error"]

    def test_veterinaria_task_status_endpoint(self, setup_test_db):
        """Test endpoint de verificación de estado de tareas."""
        response = vet_client.get("/historias-clinicas/task/test-task-123")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "task_id" in data

    def test_petshop_inventory_endpoint_response(self, setup_test_db):
        """Test que el endpoint de inventario responde correctamente."""
        # Simular archivo Excel
        from io import BytesIO

        file_content = b"mock excel content"
        files = {
            "file": (
                "test_inventory.xlsx",
                BytesIO(file_content),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }

        response = petshop_client.post("/upload-inventario/", files=files)

        assert response.status_code == 200
        data = response.json()
        assert "filename" in data
        assert "status" in data

    def test_petshop_report_generation_endpoint(self, setup_test_db):
        """Test endpoint de generación de reportes."""
        response = petshop_client.post(
            "/reportes/inventario/?store_id=1&report_type=stock_low"
        )

        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestCrossServiceWorkflow:
    """Tests de flujos de trabajo que involucran múltiples servicios."""

    def test_user_and_pet_creation_workflow(self, setup_test_db):
        """Test flujo de creación de usuario y mascota."""
        # 1. Crear usuario en servicio de auth
        user_data = {
            "email": "owner@example.com",
            "password": "testpassword",
            "roles": ["cliente"],
        }
        auth_response = auth_client.post("/users/", json=user_data)
        assert auth_response.status_code == 200
        user = auth_response.json()
        user_id = user["id"]

        # 2. Crear mascota en servicio de veterinaria vinculada al usuario
        pet_data = {
            "nombre": "Max",
            "especie": "Canino",
            "raza": "Golden Retriever",
            "edad": 3,
            "propietario_id": user_id,
        }
        vet_response = vet_client.post("/mascotas/", json=pet_data)
        assert vet_response.status_code == 200
        pet = vet_response.json()

        # Verificar que la mascota fue creada correctamente
        assert pet["nombre"] == "Max"
        assert pet["propietario_id"] == user_id

    def test_medical_report_generation_workflow(self, setup_test_db):
        """Test flujo de generación de reporte médico."""
        # Crear mascota primero
        pet_data = {
            "nombre": "Luna",
            "especie": "Felino",
            "raza": "Siamés",
            "edad": 2,
            "propietario_id": 1,
        }
        vet_client.post("/mascotas/", json=pet_data)

        # Generar reporte médico
        response = vet_client.post("/mascotas/1/reportes/")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        # El endpoint puede devolver error o processing dependiendo
        # de si Celery está disponible
        assert data["status"] in ["processing", "error"]


class TestErrorHandling:
    """Tests de manejo de errores en integración."""

    def test_veterinaria_invalid_pet_id(self, setup_test_db):
        """Test manejo de errores con ID de mascota inválido."""
        response = vet_client.get("/mascotas/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_auth_duplicate_user_email(self, setup_test_db):
        """Test manejo de error por email duplicado."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "testpassword",
            "roles": [],
        }

        # Crear primer usuario
        auth_client.post("/users/", json=user_data)

        # Intentar crear segundo usuario con mismo email
        response = auth_client.post("/users/", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_task_status_error_handling(self, setup_test_db):
        """Test manejo de errores en verificación de estado de tareas."""
        response = vet_client.get("/historias-clinicas/task/failed-task-123")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "task_id" in data
