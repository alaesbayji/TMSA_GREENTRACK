import './Featured.scss';
import MoreVertIcon from '@mui/icons-material/MoreVert';

import { useState, useEffect } from 'react';
import api from '../../Api'; // Import the Axios instance

const Featured = () => {
  const [totalEntreprises, setTotalEntreprises] = useState(0);
  const [totalEmplois, setTotalEmplois] = useState(0);
  const [totalInvestissement, setTotalInvestissement] = useState(0);
  const [totalSuperficie, setTotalSuperficie] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEntreprisesData = async () => {
      try {
        const response = await api.get('http://localhost:8000/api/entreprise/');
        const entreprises = response.data;

        // Calcul des statistiques
        const totalEmplois = entreprises.reduce((acc, entreprise) => acc + (entreprise.nombre_emploi || 0), 0);
        const totalInvestissement = entreprises.reduce((acc, entreprise) => acc + (entreprise.montant_investissement || 0), 0);
        const totalSuperficie = entreprises.reduce((acc, entreprise) => acc + (entreprise.superficie_totale || 0), 0);

        setTotalEntreprises(entreprises.length);
        setTotalEmplois(totalEmplois);
        setTotalInvestissement(totalInvestissement);
        setTotalSuperficie(totalSuperficie);
      } catch (error) {
        console.error('Erreur lors de la récupération des données des entreprises:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEntreprisesData();
  }, []);

  if (loading) {
    return <div>Chargement des statistiques...</div>;
  }

  return (
    <div className='featured'>
      <div className="top">
        <h1 className='title'>Statistiques des Entreprises</h1>
        <MoreVertIcon fontSize='small'></MoreVertIcon>
      </div>
      <div className="bottom">
        <div className="featuredChart">
         
        </div>
        <p className="title">Nombre Total d'Entreprises</p>
        <p className="amount">{totalEntreprises}</p>
        <div className="summary">
          <div className="item">
            <div className="itemTitle">Total Emplois</div>
            <div className="resultAmount">{totalEmplois}</div>
          </div>
          <div className="item">
            <div className="itemTitle">Total Investissement</div>
            <div className="resultAmount">{totalInvestissement.toLocaleString()} MAD</div>
          </div>
          <div className="item">
            <div className="itemTitle">Total Superficie</div>
            <div className="resultAmount">{totalSuperficie.toLocaleString()} m²</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Featured;