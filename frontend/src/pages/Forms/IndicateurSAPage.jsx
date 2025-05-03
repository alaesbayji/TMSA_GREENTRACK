import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './ProvincePage.scss'; // Utiliser le même fichier SCSS
import AjoutIndicateurSAForm from '../../components/Aspects/AjoutIndicateurSAForm';

const IndicateurSAPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Indicateurs Sous Aspect</h1>
        </div>
        <div className="bottom">
          <AjoutIndicateurSAForm></AjoutIndicateurSAForm>
      </div>
    </div>
    </div>
  );
};

export default IndicateurSAPage;