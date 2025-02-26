import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import ProvinceComponent from '../../components/Province/ProvinceComponent';
import CommuneComponent from '../../components/Province/CommuneComponent';
import ZoneComponent from '../../components/Province/ZoneComponent';
import './ProvincePage.scss'; // Utiliser le même fichier SCSS

const ProvincePage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Provinces, Communes et Zones</h1>
        </div>
        <div className="bottom">
          <ProvinceComponent />
          <CommuneComponent />
          <ZoneComponent />
        </div>
      </div>
    </div>
  );
};

export default ProvincePage;