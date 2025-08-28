# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos de requerimientos e instalar dependencias
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar el resto de la aplicación
COPY ./app /app/app

# El comando para correr la aplicación será provisto por docker-compose
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
