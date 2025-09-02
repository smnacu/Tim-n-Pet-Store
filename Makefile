.PHONY: help install test lint format clean docker-build docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  install      - Instalar dependencias"
	@echo "  test         - Ejecutar tests"
	@echo "  lint         - Ejecutar linting"
	@echo "  format       - Formatear código"
	@echo "  clean        - Limpiar archivos temporales"
	@echo "  docker-build - Construir contenedores Docker"
	@echo "  docker-up    - Levantar servicios con Docker Compose"
	@echo "  docker-down  - Detener servicios Docker"

install:
	pip install -r requirements.txt

test:
	@echo "🧪 Ejecutando tests..."
	export PYTHONPATH="$(PWD):$$PYTHONPATH" && pytest tests/ -v

lint:
	@echo "⚡ Ejecutando verificaciones de código..."
	export PYTHONPATH="$(PWD):$$PYTHONPATH" && \
	flake8 auth/ veterinaria/ peluqueria/ petshop/ common/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	@echo "📝 Formateando código..."
	black auth/ veterinaria/ peluqueria/ petshop/ common/ tests/
	isort auth/ veterinaria/ peluqueria/ petshop/ common/ tests/

clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.db" -delete

docker-build:
	@echo "🐳 Construyendo contenedores Docker..."
	docker compose build

docker-up:
	@echo "🚀 Levantando servicios..."
	docker compose up -d

docker-down:
	@echo "🛑 Deteniendo servicios..."
	docker compose down

# Comando para verificar todo
check: lint test
	@echo "✅ Todas las verificaciones completadas."