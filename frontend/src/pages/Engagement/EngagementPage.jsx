import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';

import './EngagementPage.scss'; // Utiliser le même fichier SCSS
import EngagementStepper from '../../components/Engagements/EngagementStepper';

const EngagementPage = () => {
  return (
    <div className="home">
      <Sidebar />
      <div className="provinceContainer">
        <Navbar />
      
        <div className="bottom">
          <EngagementStepper></EngagementStepper>
      </div>
    </div>
    </div>
  );
};

export default EngagementPage;