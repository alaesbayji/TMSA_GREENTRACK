import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './ProvincePage.scss'; // Utiliser le même fichier SCSS
import AspectComponent from '../../components/Aspects/AspectComponent';
import SousAspectComponent from '../../components/Aspects/SousAspectComponent';

const AspectPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Aspects</h1>
        </div>
        <div className="bottom">
          <AspectComponent></AspectComponent>
      </div>
    </div>
    </div>
  );
};

export default AspectPage;