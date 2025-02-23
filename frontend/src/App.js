import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext'; // Importer le contexte d'authentification
import Login from './pages/Login/Login';
import Home from './pages/Home/home';
import Add_entreprise1 from './pages/Entreprises/Add_entreprise1';
import Add_entreprise2 from './pages/Entreprises/Add_entreprise2';
import ProtectedRoute from './ProtectedRoute';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedRoute roles={['Admin', 'ResponsableEntreprise', 'ResponsableSuiviTMSA']} />}>
            <Route path="/home" element={<Home />} />
          </Route>
          <Route element={<ProtectedRoute roles={['Admin']} />}>
            <Route path="/ajouter_entreprise1" element={<Add_entreprise1 />} />
            <Route path="/ajouter_entreprise2" element={<Add_entreprise2 />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;