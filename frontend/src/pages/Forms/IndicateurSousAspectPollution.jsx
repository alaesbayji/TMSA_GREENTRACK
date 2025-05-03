import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './ProvincePage.scss'; // Utiliser le même fichier SCSS
import AjoutIndicateurEauPollution from '../../components/Aspects/AjoutIndicateurEauPollution';

const IndicateurSousAspectPollution = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />

        <div className="bottom">
          <AjoutIndicateurEauPollution></AjoutIndicateurEauPollution>
      </div>
    </div>
    </div>
  );
};

export default IndicateurSousAspectPollution;