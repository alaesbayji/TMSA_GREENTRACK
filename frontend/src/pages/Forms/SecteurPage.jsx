import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import SecteurComponent from '../../components/Province/SecteurComponent';
import ActiviteComponent from '../../components/Province/ActiviteComponent';
import './ProvincePage.scss'; // Utiliser le même fichier SCSS

const SecteurPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Secteurs et Activités</h1>
        </div>
        <div className="bottom">
          <SecteurComponent />
          <ActiviteComponent />
        </div>
      </div>
    </div>
  );
};

export default SecteurPage;