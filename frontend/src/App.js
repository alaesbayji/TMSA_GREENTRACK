import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext'; // Importer le contexte d'authentification
import Login from './pages/Login/Login';
import Home from './pages/Home/home';

import ProtectedRoute from './ProtectedRoute';
import PublicRoute from './PublicRoute'; // Nouvel import  
import AddResponsableEntreprise from './pages/Users/AddResponsableEntreprise';
import AddResponsableSuivi from './pages/Users/AddResponsableSuivi';
import ProvincePage from './pages/Forms/ProvincePage';
import SecteurPage from './pages/Forms/SecteurPage';
import Ajouter_entreprise1 from './pages/Entreprises/Ajouter_entreprise1';
import Ajouter_entreprise2 from './pages/Entreprises/Ajouter_entreprise2';
import EntrepriseMere from './pages/EntrepriseMere/EntrepriseMere';
import List from './pages/listusers/List';
import Listsuivi from './pages/listusers/Listsuivi';
import ListEntreprises from './pages/listentreprises/ListEntreprises';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
        <Route  
            path="/login"  
            element={  
              <PublicRoute>  
                <Login />  
              </PublicRoute>  
            }  
          />            <Route element={<ProtectedRoute roles={['Admin', 'ResponsableEntreprise', 'ResponsableSuiviTMSA']} />}>
            <Route path="/home" element={<Home />} />
          </Route>
          <Route element={<ProtectedRoute roles={['Admin']} />}>
          <Route path="/List_entreprise" element={<ListEntreprises />} />
            <Route path="/ajouter_entreprise1" element={<Ajouter_entreprise1 />} />
           <Route path="/ajouter_entreprise2" element={<Ajouter_entreprise2 />} />
            <Route path="/List_Responsable_entreprise" element={<List />} />
            <Route path="/List_Responsable_suivi" element={<Listsuivi />} />
            <Route path="/ajouter_responsable_entreprise" element={<AddResponsableEntreprise />} />
            <Route path="/ajouter_responsable_suivi" element={<AddResponsableSuivi />} />
            <Route path="/Province" element={<ProvincePage/>} />
            <Route path="/Commune" element={<SecteurPage/>} />
            <Route path="/entreprise-mere" element={<EntrepriseMere/>} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;