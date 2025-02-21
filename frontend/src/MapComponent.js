// MapComponent.js  
import React from 'react';  
import { useNavigate } from 'react-router-dom';  
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';  
import 'leaflet/dist/leaflet.css';  
import './MapComponent.css'; // Import the CSS file  
import Sidebar from './components/Sidebar'; // Assurez-vous que le chemin est correct  
import Navbar from './components/Navbar';  

function MapComponent() {  
  const navigate = useNavigate(); // Hook for navigation  

  const handleLogout = () => {  
    console.log('User logged out');  
    navigate('/'); // Navigate back to the LoginPage  
  };  

  return (  
    <div className="map-container">  
      <Sidebar />  
      <Navbar /> {/* Ajout de la Navbar ici */}  
      <div className="map-section">  
        <button onClick={handleLogout} className="logoutButton">  
          Logout  
        </button>  
        <MapContainer center={[35.6895, -5.9078]} zoom={13} style={{ height: "500px", width: "100%" }}>  
          <TileLayer  
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"  
          />  
          <Marker position={[35.6895, -5.9078]}>  
            <Popup>Test popup</Popup>  
          </Marker>  
        </MapContainer>  
      </div>  
    </div>  
  );  
}  

export default MapComponent;