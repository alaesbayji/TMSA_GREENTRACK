import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './ProvincePage.scss'; // Utiliser le même fichier SCSS
import AjoutIndicateurForm from '../../components/Aspects/AjoutIndicateurForm';

const IndicateurPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Aspects</h1>
        </div>
        <div className="bottom">
          <AjoutIndicateurForm></AjoutIndicateurForm>
      </div>
    </div>
    </div>
  );
};

export default IndicateurPage;