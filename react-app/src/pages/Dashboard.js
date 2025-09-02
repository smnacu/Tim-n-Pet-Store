import React from 'react';

const Dashboard = ({ services }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return 'var(--color-success)';
      case 'offline': return 'var(--color-danger)';
      case 'loading': return 'var(--color-warning)';
      default: return 'var(--color-text-light)';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'online': return 'En línea';
      case 'offline': return 'Sin conexión';
      case 'loading': return 'Verificando...';
      default: return 'Desconocido';
    }
  };

  return (
    <div className="dashboard">
      <h1>Panel de Control - Timón Pet Store</h1>
      <p>Plataforma integral de gestión para tiendas de mascotas</p>
      
      <div className="services-grid">
        {Object.entries(services).map(([key, service]) => (
          <div key={key} className="service-card">
            <h3>{service.name}</h3>
            <p>{service.description}</p>
            <div className="service-status">
              <div 
                className={`status-indicator ${service.status}`}
                style={{ backgroundColor: getStatusColor(service.status) }}
              ></div>
              <span>{getStatusText(service.status)}</span>
              <span style={{ marginLeft: 'auto', color: 'var(--color-text-light)' }}>
                Puerto: {service.port}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2>Características del Sistema</h2>
        <ul>
          <li><strong>Autenticación:</strong> Sistema JWT con roles (veterinario, peluquero, admin, cliente)</li>
          <li><strong>Veterinaria:</strong> Gestión de historiales clínicos, consultas y documentos</li>
          <li><strong>Peluquería:</strong> Sistema de turnos y gestión de servicios</li>
          <li><strong>Pet Shop:</strong> Inventario, proveedores y punto de venta</li>
          <li><strong>Base de Datos:</strong> PostgreSQL con esquemas separados por microservicio</li>
          <li><strong>Arquitectura:</strong> Microservicios con FastAPI y React</li>
        </ul>
      </div>

      <div className="card">
        <h2>API Documentation</h2>
        <p>Los endpoints de documentación están disponibles en:</p>
        <ul>
          <li><a href="http://localhost:8001/docs" target="_blank" rel="noopener noreferrer">Auth Service - Swagger UI</a></li>
          <li><a href="http://localhost:8002/docs" target="_blank" rel="noopener noreferrer">Veterinaria Service - Swagger UI</a></li>
          <li><a href="http://localhost:8003/docs" target="_blank" rel="noopener noreferrer">Peluquería Service - Swagger UI</a></li>
          <li><a href="http://localhost:8004/docs" target="_blank" rel="noopener noreferrer">Pet Shop Service - Swagger UI</a></li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;