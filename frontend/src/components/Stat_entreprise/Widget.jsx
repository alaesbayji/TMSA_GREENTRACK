import './Widget.scss';
import BusinessIcon from '@mui/icons-material/Business';
import WorkOutlineOutlinedIcon from '@mui/icons-material/WorkOutlineOutlined';
import MonetizationOnOutlinedIcon from '@mui/icons-material/MonetizationOnOutlined';
import SquareFootOutlinedIcon from '@mui/icons-material/SquareFootOutlined';
import { useState, useEffect } from 'react';
import api from '../../Api'; // Import the Axios instance

const Widget = ({ type }) => {
  const [data, setData] = useState({ title: '', icon: null, link: '', isMoney: false });
  const [count, setCount] = useState(0); // State for the count (number of entreprises, emplois, etc.)

  useEffect(() => {
    // Fetch data from the API depending on the type of widget
    const fetchData = async () => {
      try {
        const response = await api.get('http://localhost:8000/api/entreprise/');
        const entreprises = response.data;

        switch (type) {
          case 'entreprises':
            setCount(entreprises.length); // Nombre total d'entreprises
            break;
          case 'emplois':
            const totalEmplois = entreprises.reduce((sum, entreprise) => sum + (entreprise.nombre_emploi || 0), 0);
            setCount(totalEmplois); // Nombre total d'emplois
            break;
          case 'investissements':
            const totalInvestissements = entreprises.reduce((sum, entreprise) => sum + (entreprise.montant_investissement || 0), 0);
            setCount(totalInvestissements); // Montant total des investissements
            break;
          case 'superficie':
            const totalSuperficie = entreprises.reduce((sum, entreprise) => sum + (entreprise.superficie_totale || 0), 0);
            setCount(totalSuperficie); // Superficie totale
            break;
          default:
            break;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [type]);

  useEffect(() => {
    // Setup widget data based on type
    switch (type) {
      case 'entreprises':
        setData({
          title: 'Entreprises',
          isMoney: false,
          link: 'Voir toutes les entreprises',
          icon: <BusinessIcon className='icon' style={{
            color: 'blue',
            backgroundColor: 'rgba(0,0,255,0.2)',
          }} />,
        });
        break;
      case 'emplois':
        setData({
          title: 'Emplois',
          isMoney: false,
          link: 'Voir les emplois',
          icon: <WorkOutlineOutlinedIcon className='icon' style={{
            color: 'green',
            backgroundColor: 'rgba(0,255,0,0.2)',
        

          }} />,
        });
        break;
      case 'investissements':
        setData({
          title: 'Investissements',
          isMoney: true,
          link: 'Voir les investissements',
          icon: <MonetizationOnOutlinedIcon className='icon' style={{
            color: 'goldenrod',
            backgroundColor: 'rgba(218,165,32,0.2)',
          }} />,
        });
        break;
      case 'superficie':
        setData({
          title: 'Superficie (m²)',
          isMoney: false,
          link: 'Voir la superficie',
          icon: <SquareFootOutlinedIcon className='icon' style={{
            color: 'purple',
            backgroundColor: 'rgba(128,0,128,0.2)',
          }} />,
        });
        break;
      default:
        break;
    }
  }, [type]);

  return (
    <div className='widget'>
      <div className="left">
        <span className="title">{data.title}</span>
        <span className="counter">{count} {data.isMoney && "MAD"}</span>
      </div>
      <div className="right">
        {data.icon}
      </div>
    </div>
  );
};

export default Widget;