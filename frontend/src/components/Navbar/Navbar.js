import React, { useState } from 'react';
import { useAuth } from '../../AuthContext';
import { useNavigate } from 'react-router-dom';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import LanguageIcon from '@mui/icons-material/Language';
import alae from '../../images/alae.jpg'; // Image par défaut
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth(); // Utiliser le contexte d'authentification
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  // Toggle dropdown visibility
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  // Gérer la déconnexion
  const handleLogout = () => {
    logout(); // Appeler la fonction de déconnexion du contexte
    navigate('/login'); // Rediriger vers la page de connexion
  };

  return (
    <div className="navbar">
      <div className="wrapper">
      Bonjour {user ? user.nom : 'USER'} 

        <div className="search">
          {/* Afficher le nom de l'utilisateur */}
          <input type='text' placeholder='Search ...' />  
          <SearchOutlinedIcon />  
        </div>

        <div className="items">
          <div className="item">
            <LanguageIcon className="icon" />
            Francais
          </div>
          <div className="item">
            <DarkModeIcon className="icon" />
          </div>
          <div className="item">
            <FormatListBulletedIcon className="icon" />
          </div>

          {/* Dropdown pour le profil */}
          <div className="profile-dropdown">
            <div className="profile-dropdown-btn" onClick={toggleDropdown}>
              <div className="profile-img">
                <img
                  src={user?.profile_photo ? `data:image/jpeg;base64,${user.profile_photo}` : alae}
                  alt="Profile"
                  className="avatar"
                />
              </div>
            </div>

            {isDropdownOpen && (
              <ul className="profile-dropdown-list">
                <li className="profile-dropdown-list-item">
                  <a href="/profile">Profil</a>
                </li>
                <hr />
                <li className="profile-dropdown-list-item" onClick={handleLogout}>
                  <a href="/login">Déconnexion</a>
                </li>
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;