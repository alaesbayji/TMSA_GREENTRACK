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
import EditResponsableEntreprise from './pages/Users/EditResponsableEntreprise';
import EditResponsableSuivi from './pages/Users/EditResponsableSuivi';
import EditEntreprise from './pages/Entreprises/EditEntreprise';
import AspectPage from './pages/Forms/AspectPage';
import SousAspectPage from './pages/Forms/SousAspectPage';
import IndicateurPage from './pages/Forms/IndicateurPage';
import IndicateurSousAspectPollution from './pages/Forms/IndicateurSousAspectPollution';
import IndicateurSAPage from './pages/Forms/IndicateurSAPage';
import EngagementStepper from './components/Engagements/EngagementStepper';
import EngagementPage from './pages/Engagement/EngagementPage';

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
          />  
          <Route element={<ProtectedRoute roles={['Admin', 'ResponsableEntreprise', 'ResponsableSuiviTMSA']} />}>  
            <Route path="/home" element={<Home />} />  

            {/* Route for user list with dynamic userId */}  

            {/* Route for entreprise list with dynamic entrepriseId */}  
            <Route path="/list_entreprise" element={<ListEntreprises />} />  
            <Route path="/entreprise/:id" element={<EditEntreprise />} />  

            <Route path="/ajouter_entreprise1" element={<Ajouter_entreprise1 />} />  
            <Route path="/ajouter_entreprise2" element={<Ajouter_entreprise2 />} />  
            <Route path="/List_Responsable_entreprise" element={<List />} /> 
            <Route path="/users/:id" element={<EditResponsableEntreprise />} />  
            <Route path="/res_suivi/:id" element={<EditResponsableSuivi />} />  
 
            <Route path="/List_Responsable_suivi" element={<Listsuivi />} />  
            <Route path="/ajouter_responsable_entreprise" element={<AddResponsableEntreprise />} />  
            <Route path="/ajouter_responsable_suivi" element={<AddResponsableSuivi />} />  
            <Route path="/Province" element={<ProvincePage />} />  
            <Route path="/Commune" element={<SecteurPage />} />  
            <Route path="/aspect" element={<AspectPage />} />  
            <Route path="/sous_aspect" element={<SousAspectPage />} />  
            <Route path="/indicateur" element={<IndicateurPage />} />  
            <Route path="/indicateurpollution" element={<IndicateurSousAspectPollution />} />  
            <Route path="/indicateursousaspect" element={<IndicateurSAPage />} />  
            <Route path="/entreprise-mere" element={<EntrepriseMere />} />  
            <Route path="/engagements" element={<EngagementPage />} />  
          </Route>  
        </Routes>  
      </Router>  
    </AuthProvider>  
  );  
};  

export default App;  