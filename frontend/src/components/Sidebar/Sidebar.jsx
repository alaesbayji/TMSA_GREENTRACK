import React from 'react';
import './Sidebar.scss';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import MapIcon from '@mui/icons-material/Map';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ApartmentIcon from '@mui/icons-material/Apartment';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import ChecklistIcon from '@mui/icons-material/Checklist';
import EventIcon from '@mui/icons-material/Event';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import AvTimerIcon from '@mui/icons-material/AvTimer';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import SouthAmericaIcon from '@mui/icons-material/SouthAmerica';
import ConstructionIcon from '@mui/icons-material/Construction';
import logo from '../../images/1.png';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    console.log('User logged out');
    navigate('/');
  };

  const isActive = (...paths) => paths.includes(location.pathname);

  return (
    <div className='sidebar'>
      <div className='top'>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <img src={logo} alt="Tanger Med Monitoring" className="logo" />
        </Link>
      </div>
      <hr />
      <div className='center'>
        <ul>
          <p className="title">Navigation</p>
          <Link to="/dashboard" style={{ textDecoration: 'none' }}>
            <li className={isActive('/dashboard') ? 'active' : ''}>
              <DashboardIcon className="icon" />
              <span>Dashboard</span>
            </li>
          </Link>
          <Link to="/map" style={{ textDecoration: 'none' }}>
            <li className={isActive('/map') ? 'active' : ''}>
              <MapIcon className="icon" />
              <span>Map</span>
            </li>
          </Link>
          <Link to="/List_entreprise" style={{ textDecoration: 'none' }}>
            <li className={isActive('/List_entreprise','/ajouter_entreprise1', '/ajouter_entreprise2') ? 'active' : ''}>
              <ApartmentIcon className="icon" />
              <span>Entreprises</span>
            </li>
          </Link>
          <Link to="/List_Responsable_entreprise" style={{ textDecoration: 'none' }}>
            <li className={isActive('/ajouter_responsable_entreprise','/List_Responsable_entreprise') ? 'active' : ''}>
              <PersonAddIcon className="icon" />
              <span>Responsable Entreprise</span>
            </li>
          </Link>
          <Link to="/List_Responsable_suivi" style={{ textDecoration: 'none' }}>
            <li className={isActive('/ajouter_responsable_suivi','/List_Responsable_suivi') ? 'active' : ''}>
              <ManageAccountsIcon className="icon" />
              <span>Responsable Suivi</span>
            </li>
          </Link>

          <p className="title">Fonctionnalités</p>
          <Link to="/engagement" style={{ textDecoration: 'none' }}>
            <li className={isActive('/engagement') ? 'active' : ''}>
              <ChecklistIcon className="icon" />
              <span>Engagement</span>
            </li>
          </Link>
          <Link to="/suivis" style={{ textDecoration: 'none' }}>
            <li className={isActive('/suivis') ? 'active' : ''}>
              <EventIcon className="icon" />
              <span>Suivis</span>
            </li>
          </Link>
          <Link to="/rapports" style={{ textDecoration: 'none' }}>
            <li className={isActive('/rapports') ? 'active' : ''}>
              <PictureAsPdfIcon className="icon" />
              <span>Rapports</span>
            </li>
          </Link>

          <p className="title">Options</p>
          <Link to="/aspect" style={{ textDecoration: 'none' }}>
            <li className={isActive('/aspect') ? 'active' : ''}>
              <SouthAmericaIcon className="icon" />
              <span>Aspect</span>
            </li>
          </Link>
          <Link to="/indicateurs" style={{ textDecoration: 'none' }}>
            <li className={isActive('/indicateurs') ? 'active' : ''}>
              <AvTimerIcon className="icon" />
              <span>Indicateurs</span>
            </li>
          </Link>
          <Link to="/Province" style={{ textDecoration: 'none' }}>
            <li className={isActive('/Province') ? 'active' : ''}>
              <LocationOnIcon className="icon" />
              <span>Provinces, Communes et Zones</span>
            </li>
          </Link>
          <Link to="/Commune" style={{ textDecoration: 'none' }}>
            <li className={isActive('/Commune') ? 'active' : ''}>
              <ConstructionIcon className="icon" />
              <span>Secteurs et Activités</span>
            </li>
          </Link>

          <p className="title">Paramètres</p>
          <Link to="/settings" style={{ textDecoration: 'none' }}>
            <li className={isActive('/settings') ? 'active' : ''}>
              <SettingsIcon className="icon" />
              <span>Settings</span>
            </li>
          </Link>
          <li onClick={handleLogout} style={{ cursor: 'pointer' }}>
            <LogoutIcon className="icon" />
            <span>Logout</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;