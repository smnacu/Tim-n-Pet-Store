import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Timón Pet Store</h1>
        <p>Plataforma de Gestión</p>
        <div>
          <h2>Microservicios:</h2>
          <ul>
            <li>Auth Service: Running</li>
            <li>Veterinaria Service: Running</li>
            <li>Peluqueria Service: Running</li>
            <li>Petshop Service: Running</li>
          </ul>
        </div>
      </header>
    </div>
  );
}

export default App;
