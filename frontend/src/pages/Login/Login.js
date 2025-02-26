import React, { useState } from 'react';
import { useAuth } from '../../AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
import image from '../../images/2.png';
import shape from '../../images/shape.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email,
        password,
      });
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
  
      if (response.data.user) {
        login(response.data.user); // Mettre à jour l'état de l'utilisateur
        navigate('/home'); // Rediriger vers la page d'accueil
      } else {
        setError('Identifiants invalides');
      }
    } catch (err) {
      setError('Erreur de connexion');
    }
  };

  return (
    <div className="login-container">
      <div className="logo-section">
        <img src={image} className="logo" alt="Logo" />
        <button className="read-more-button">Read More</button>
        <img src={shape} className="logo1" alt="Shape" />
      </div>

      <div className="login-form">
        <h2>Hello Again!</h2>
        <p>Welcome Back</p>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="input"
          />
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
        <p className="forgot-password">Forgot Password?</p>
      </div>
    </div>
  );
};

export default Login;