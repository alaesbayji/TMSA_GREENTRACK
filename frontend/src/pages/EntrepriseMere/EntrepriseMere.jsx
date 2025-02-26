import React from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import EntrepriseMereComponents from '../../components/Entreprise/EntrepriseMereComponents'; // Import du composant enfant
import './EntrepriseMere.scss'; // Utiliser le même fichier SCSS

const EntrepriseMere = () => {
  return (
    <div className="new">
      <Sidebar />
      <div className="newContainer">
        <Navbar />
        <div className="top">
          <h1>Gestion des Entreprises Mères</h1>
        </div>
        <div className="bottom">
          <EntrepriseMereComponents /> {/* Inclusion du composant enfant */}
        </div>
      </div>
    </div>
  );
};

export default EntrepriseMere;