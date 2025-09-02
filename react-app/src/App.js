import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  const [services, setServices] = useState({
    auth: { status: 'loading', name: 'Autenticación', port: 8001, description: 'Gestión de usuarios y roles' },
    veterinaria: { status: 'loading', name: 'Veterinaria', port: 8002, description: 'Historiales clínicos y consultas' },
    peluqueria: { status: 'loading', name: 'Peluquería', port: 8003, description: 'Gestión de turnos y servicios' },
    petshop: { status: 'loading', name: 'Pet Shop', port: 8004, description: 'Inventario y punto de venta' }
  });

  useEffect(() => {
    // Función para verificar el estado de los servicios
    const checkServiceStatus = async (serviceName, port) => {
      try {
        const response = await fetch(`http://localhost:${port}/`, {
          method: 'GET',
          timeout: 5000
        });
        
        if (response.ok) {
          setServices(prev => ({
            ...prev,
            [serviceName]: { ...prev[serviceName], status: 'online' }
          }));
        } else {
          setServices(prev => ({
            ...prev,
            [serviceName]: { ...prev[serviceName], status: 'offline' }
          }));
        }
      } catch (error) {
        setServices(prev => ({
          ...prev,
          [serviceName]: { ...prev[serviceName], status: 'offline' }
        }));
      }
    };

    // Verificar estado inicial de todos los servicios
    Object.entries(services).forEach(([serviceName, service]) => {
      checkServiceStatus(serviceName, service.port);
    });

    // Verificar periódicamente el estado de los servicios
    const interval = setInterval(() => {
      Object.entries(services).forEach(([serviceName, service]) => {
        checkServiceStatus(serviceName, service.port);
      });
    }, 30000); // Cada 30 segundos

    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="App">
        <Header />
        <div className="App-main">
          <Sidebar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard services={services} />} />
              <Route path="/veterinary" element={<div>Módulo Veterinaria (En desarrollo)</div>} />
              <Route path="/grooming" element={<div>Módulo Peluquería (En desarrollo)</div>} />
              <Route path="/petshop" element={<div>Módulo Pet Shop (En desarrollo)</div>} />
              <Route path="/clients" element={<div>Módulo Clientes (En desarrollo)</div>} />
              <Route path="/login" element={<div>Login (En desarrollo)</div>} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
