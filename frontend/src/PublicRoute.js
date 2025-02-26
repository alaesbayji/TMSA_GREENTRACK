import React from 'react';  
import { Navigate } from 'react-router-dom';  
import { useAuth } from './AuthContext';  

const PublicRoute = ({ children }) => {  
  const { user } = useAuth();  

  // Si l'utilisateur est connecté, redirige vers la page "/home"  
  if (user) {  
    return <Navigate to="/home" />;  
  }  

  // Sinon, permet d'accéder à la page publique  
  return children;  
};  

export default PublicRoute;