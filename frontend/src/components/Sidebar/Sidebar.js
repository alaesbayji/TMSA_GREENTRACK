// Sidebar.js  
import React from 'react';  
import './Sidebar.css'; // Importer le fichier CSS  
import logo from '../../images/1.png'; // Assurez-vous d'ajuster le chemin de l'image  
import { useNavigate, useLocation } from 'react-router-dom';  
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
    const location = useLocation(); // Hook for getting the current location  

    const handleLogout = () => {  
        console.log('User logged out');  
        navigate('/'); // Navigate back to the LoginPage  
    };  

    // Function to determine if the link is active  
    const isActive = (...paths) => paths.includes(location.pathname);  

    return (  
        <div className="sidebar">  
            <div className="logo-section2">  
                <img src={logo} alt="Tanger Med Monitoring" className="logo2" />  
            </div>  
            <nav className="nav-links">  
                <a href="/dashboard" className={`nav-item ${isActive('/dashboard') ? 'active' : ''}`}>  
                    <DashboardIcon style={{ marginRight: '8px' }}/> Dashboard  
                </a>  
                <a href="/map" className={`nav-item ${isActive('/map') ? 'active' : ''}`}>  
                    <MapIcon style={{ marginRight: '8px' }} /> Map  
                </a>  
                <a href="/ajouter_entreprise1" className={`nav-item ${isActive('/ajouter_entreprise1','/ajouter_entreprise2') ? 'active' : ''}`}>  
                    <ApartmentIcon style={{ marginRight: '8px' }} /> Entreprises  
                </a>  
                <a href="/responsable-entreprise" className={`nav-item ${isActive('/responsable-entreprise') ? 'active' : ''}`}>  
                    <PersonAddIcon style={{ marginRight: '8px' }} /> Responsable Entreprise  
                </a>  
                <a href="/responsable-suivi" className={`nav-item ${isActive('/responsable-suivi') ? 'active' : ''}`}>  
                    <ManageAccountsIcon style={{ marginRight: '8px' }} /> Responsable Suivi  
                </a>  
            </nav>  
            <div className="features-section">  
                <h4>Fonctionnalités</h4>  
                <a href="/engagement" className={`nav-item ${isActive('/engagement') ? 'active' : ''}`}>  
                    <ChecklistIcon style={{ marginRight: '8px' }} /> Engagement  
                </a>  
                <a href="/suivis" className={`nav-item ${isActive('/suivis') ? 'active' : ''}`}>  
                    <EventIcon style={{ marginRight: '8px' }} /> Suivis  
                </a>  
                <a href="/rapports" className={`nav-item ${isActive('/rapports') ? 'active' : ''}`}>  
                    <PictureAsPdfIcon style={{ marginRight: '8px' }} /> Rapports  
                </a>  
            </div>  
            <div className="options-section">  
                <h4>Options</h4>  
                <a href="/aspect" className={`nav-item ${isActive('/aspect') ? 'active' : ''}`}>  
                    <SouthAmericaIcon style={{ marginRight: '8px' }} /> Aspect  
                </a>  
                <a href="/indicateurs" className={`nav-item ${isActive('/indicateurs') ? 'active' : ''}`}>  
                    <AvTimerIcon style={{ marginRight: '8px' }} /> Indicateurs  
                </a>  
                <a href="/provinces" className={`nav-item ${isActive('/provinces') ? 'active' : ''}`}>  
                    <TerrainIcon style={{ marginRight: '8px' }} /> Provinces  
                </a>  
                <a href="/communes" className={`nav-item ${isActive('/communes') ? 'active' : ''}`}>  
                    <LocationOnIcon style={{ marginRight: '8px' }} /> Communes  
                </a>  
            </div>  
            <div className="settings-section">  
                <a href="/settings" className={`nav-item ${isActive('/settings') ? 'active' : ''}`}>  
                    <SettingsIcon style={{ marginRight: '8px' }} /> Settings  
                </a>  
                <a href="#" className="nav-item" onClick={handleLogout}>  
                    <LogoutIcon style={{ marginRight: '8px' }} /> Logout  
                </a>  
            </div>  
        </div>  
    );  
};  

export default Sidebar;