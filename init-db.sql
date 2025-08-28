-- Este script se ejecuta cuando el contenedor de PostgreSQL se inicia por primera vez.
-- No es necesario crear la base de datos 'timon_petstore' aquí,
-- ya que se creará a través de la variable de entorno POSTGRES_DB en docker-compose.yml.

-- Crear esquemas para cada microservicio para soportar un futuro modelo multi-inquilino.
-- Cada microservicio gestionará sus tablas dentro de su propio esquema.
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS veterinary;
CREATE SCHEMA IF NOT EXISTS grooming;
CREATE SCHEMA IF NOT EXISTS petshop;

-- Otorga privilegios al usuario 'user' sobre los nuevos esquemas.
-- Esto es crucial para que los microservicios puedan crear y acceder a sus tablas.
GRANT ALL PRIVILEGES ON SCHEMA users TO "user";
GRANT ALL PRIVILEGES ON SCHEMA veterinary TO "user";
GRANT ALL PRIVILEGES ON SCHEMA grooming TO "user";
GRANT ALL PRIVILEGES ON SCHEMA petshop TO "user";
