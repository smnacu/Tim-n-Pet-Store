# Tim-n-Pet-Store

**Plataforma integral de gestión para tiendas de mascotas** - Sistema SaaS de microservicios para portafolio personal.

## 🏗️ Arquitectura

Este proyecto implementa una arquitectura de microservicios con:

- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Base de Datos**: PostgreSQL con esquemas separados
- **Autenticación**: JWT con roles
- **Containerización**: Docker & Docker Compose

## 🚀 Servicios

### 🔐 Servicio de Autenticación (Puerto 8001)
- Gestión de usuarios y roles (veterinario, peluquero, admin, cliente)
- Autenticación JWT
- Control de acceso basado en roles

### 🏥 Servicio de Veterinaria (Puerto 8002)
- Gestión de mascotas e historiales clínicos
- Consultas veterinarias
- Documentos médicos (radiografías, análisis)
- Procesamiento OCR para digitalizar historiales

### ✂️ Servicio de Peluquería (Puerto 8003)
- Sistema de turnos y citas
- Gestión de peluqueros
- Catálogo de servicios de peluquería
- Control de disponibilidad

### 🛒 Servicio de Pet Shop (Puerto 8004)
- Gestión de inventario y productos
- Sistema de proveedores
- Punto de venta (TPV)
- Procesamiento de archivos Excel para inventario

### 🖥️ Frontend React (Puerto 3000)
- Dashboard con monitoreo de servicios
- Interfaz unificada para todos los módulos
- Navegación intuitiva
- Responsive design

## 🛠️ Instalación y Uso

### Prerrequisitos
- Docker y Docker Compose
- Node.js 16+ (para desarrollo del frontend)
- Python 3.9+ (para desarrollo del backend)

### 1. Clonar el repositorio
```bash
git clone https://github.com/smnacu/Tim-n-Pet-Store.git
cd Tim-n-Pet-Store
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con los valores apropiados
```

### 3. Levantar servicios con Docker
```bash
# Opción 1: Usar Makefile
make docker-up

# Opción 2: Docker Compose directamente
docker compose up -d
```

### 4. Verificar servicios
Los servicios estarán disponibles en:
- **Frontend**: http://localhost:3000
- **Auth API**: http://localhost:8001
- **Veterinaria API**: http://localhost:8002
- **Peluquería API**: http://localhost:8003
- **Pet Shop API**: http://localhost:8004

## 📚 Documentación API

Cada servicio tiene documentación Swagger automática:
- Auth: http://localhost:8001/docs
- Veterinaria: http://localhost:8002/docs
- Peluquería: http://localhost:8003/docs
- Pet Shop: http://localhost:8004/docs

## 🧪 Testing y Calidad de Código

### Ejecutar tests
```bash
make test
# o
./run_checks.sh
```

### Verificar calidad de código
```bash
make lint
```

### Formatear código
```bash
make format
```

### Ejecutar todas las verificaciones
```bash
make check
```

## 🗄️ Base de Datos

El sistema utiliza PostgreSQL con esquemas separados:
- `users`: Usuarios y roles
- `veterinary`: Datos veterinarios
- `grooming`: Datos de peluquería  
- `petshop`: Inventario y ventas

## 🔧 Desarrollo

### Instalar dependencias de desarrollo
```bash
make install
```

### Estructura del proyecto
```
├── auth/              # Servicio de autenticación
├── veterinaria/       # Servicio veterinario
├── peluqueria/        # Servicio de peluquería
├── petshop/          # Servicio de tienda
├── react-app/        # Frontend React
├── common/           # Utilidades compartidas
├── tests/            # Tests automatizados
└── docker-compose.yml
```

## 🚦 Estado del Proyecto

- ✅ Autenticación JWT completa
- ✅ CRUD completo para todos los servicios
- ✅ Frontend con React y navegación
- ✅ Base de datos con esquemas separados
- ✅ Tests básicos
- ✅ Linting y formateo de código
- 🔄 Integración de Celery/Redis (en progreso)
- 🔄 Procesamiento OCR (en progreso)
- 🔄 Tests de integración (en progreso)

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto es de uso educativo y portafolio personal.

## 📧 Contacto

- Proyecto: [Tim-n-Pet-Store](https://github.com/smnacu/Tim-n-Pet-Store)
- Autor: [@smnacu](https://github.com/smnacu)
