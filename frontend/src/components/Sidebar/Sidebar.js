// Sidebar.js  
import React from 'react';  
import './Sidebar.css'; // Importer le fichier CSS  
import logo from '../../images/1.png'; // Assurez-vous d'ajuster le chemin de l'image  
import { useNavigate } from 'react-router-dom';  
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
import TerrainIcon from '@mui/icons-material/Terrain';
import SouthAmericaIcon from '@mui/icons-material/SouthAmerica';
const Sidebar = () => {  
    const navigate = useNavigate(); // Hook for navigation  
    const handleLogout = () => {  
        console.log('User logged out');  
        navigate('/'); // Navigate back to the LoginPage  
      };  
    
    return (  
        <div className="sidebar">  
            <div className="logo-section2">  
                <img src={logo} alt="Tanger Med Monitoring" className="logo2" />  
            </div>  
            <nav className="nav-links">  
                <a href="#" className="nav-item"><DashboardIcon style={{ marginRight: '8px' }}/>  Dashboard</a>  
                <a href="#" className="nav-item "> <MapIcon style={{ marginRight: '8px' }}></MapIcon> Map</a>  
                <a href="#" className="nav-item active"><ApartmentIcon style={{ marginRight: '8px' }} /> Entreprises</a>  
                <a href="#" className="nav-item "><PersonAddIcon style={{ marginRight: '8px' }} /> Responsable Entreprise</a>  
                <a href="#" className="nav-item"><ManageAccountsIcon style={{ marginRight: '8px' }}/> Responsable Suivi</a>  
            </nav>  
            <div className="features-section">  
                <h4>Fonctionnalités</h4>  
                <a href="#" className="nav-item"> <ChecklistIcon style={{ marginRight: '8px' }} />Engagement</a>  
                <a href="#" className="nav-item"> <EventIcon style={{ marginRight: '8px' }} />  Suivis</a>  
                <a href="#" className="nav-item"> <PictureAsPdfIcon style={{ marginRight: '8px' }} /> Rapports</a>  
            </div>  
            <div className="options-section">  
                <h4> Options</h4>  
                <a href="#" className="nav-item"> <SouthAmericaIcon style={{ marginRight: '8px' }} />Aspect</a>  
                <a href="#" className="nav-item"> <AvTimerIcon style={{ marginRight: '8px' }} />Indicateurs</a>  
                <a href="#" className="nav-item">  <TerrainIcon style={{ marginRight: '8px' }} />Provinces</a>  
                <a href="#" className="nav-item">  <LocationOnIcon style={{ marginRight: '8px' }} />Communes</a>  
            </div>  
            <div className="settings-section">  
                <a href="#" className="nav-item">  <SettingsIcon style={{ marginRight: '8px' }} />Settings</a>  
                <a href="#" className="nav-item" onClick={handleLogout}><LogoutIcon style={{ marginRight: '8px' }} /> Logout</a>  
            </div>  
        </div>  
    );  
};  

export default Sidebar;