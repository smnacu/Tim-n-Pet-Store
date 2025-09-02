"""
Configuración de Celery para procesamiento asíncrono de tareas.
"""

from celery import Celery
import os

# Configuración de Redis como broker y backend de resultados
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Crear la aplicación Celery
celery_app = Celery(
    "timon_petstore",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "veterinaria.app.tasks",
        "petshop.app.tasks",
    ]
)

# Configuración adicional
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_routes={
        "veterinaria.app.tasks.*": {"queue": "veterinaria"},
        "petshop.app.tasks.*": {"queue": "petshop"},
    },
)

if __name__ == "__main__":
    celery_app.start()