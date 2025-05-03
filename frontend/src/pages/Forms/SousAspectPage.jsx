import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './ProvincePage.scss'; // Utiliser le même fichier SCSS
import SousAspectComponent from '../../components/Aspects/SousAspectComponent';

const SousAspectPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Sous Aspects</h1>
        </div>
        <div className="bottom">
          <SousAspectComponent></SousAspectComponent>
      </div>
    </div>
    </div>
  );
};

export default SousAspectPage;