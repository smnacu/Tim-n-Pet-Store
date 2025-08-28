import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/images/logo.svg';
import './Header.css';

const Header = () => {
  return (
    <header className="app-header">
      <div className="logo-container">
        <img src={logo} alt="Timón Pet Store Logo" className="logo-img" />
        <span className="logo-text">Timón Pet Store</span>
      </div>
      <nav>
        <Link to="/login">Login</Link>
      </nav>
    </header>
  );
};

export default Header;
