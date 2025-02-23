import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext';

const ProtectedRoute = ({ roles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Chargement...</div>; // Afficher un spinner ou un message de chargement
  }

  if (!user) {
    return <Navigate to="/" />; // Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/home" />; // Rediriger vers une page d'accueil ou une page d'erreur si l'utilisateur n'a pas le bon rôle
  }

  return <Outlet />; // Afficher la route protégée
};

export default ProtectedRoute;