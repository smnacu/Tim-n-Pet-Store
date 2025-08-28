import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="app-sidebar">
      <nav>
        <ul>
          <li><NavLink to="/" end>Dashboard</NavLink></li>
          <li><NavLink to="/veterinary">Veterinaria</NavLink></li>
          <li><NavLink to="/grooming">Peluquería</NavLink></li>
          <li><NavLink to="/petshop">Tienda</NavLink></li>
          <li><NavLink to="/clients">Clientes</NavLink></li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
