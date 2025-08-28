-- Crear bases de datos para cada microservicio
CREATE DATABASE veterinaria_db;
CREATE DATABASE peluqueria_db;
CREATE DATABASE petshop_db;
-- La base de datos 'auth_db' se crea por defecto a través de las variables de entorno de Docker.
-- Conectar a cada base de datos para crear esquemas si se desea un futuro multi-inquilino.
-- Ejemplo para la base de datos de veterinaria:
\c veterinaria_db;
-- CREATE SCHEMA tenant1;
-- CREATE SCHEMA tenant2;
-- Este es un placeholder para una futura implementación multi-inquilino.
-- La lógica para gestionar los esquemas deberá ser implementada en el microservicio correspondiente.
