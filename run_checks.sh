#!/bin/bash

# Script para ejecutar tests y verificaciones de calidad de código

echo "🔍 Ejecutando verificaciones de calidad de código..."

# Configurar PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

echo "📝 Ejecutando Black (formateo de código)..."
black --check --diff auth/ veterinaria/ peluqueria/ petshop/ common/ tests/

echo "📦 Ejecutando isort (ordenamiento de imports)..."
isort --check-only --diff auth/ veterinaria/ peluqueria/ petshop/ common/ tests/

echo "⚡ Ejecutando Flake8 (linting)..."
flake8 auth/ veterinaria/ peluqueria/ petshop/ common/ tests/ --max-line-length=88 --extend-ignore=E203,W503

echo "🧪 Ejecutando tests..."
pytest tests/ -v

echo "✅ Verificaciones completadas."