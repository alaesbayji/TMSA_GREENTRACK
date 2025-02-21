// MapComponent.js  
import React from 'react';  
import { useNavigate } from 'react-router-dom';  
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';  
import 'leaflet/dist/leaflet.css';  
import './add_Entreprise.css'; // Import the CSS file  
import Sidebar from '../../components/Sidebar/Sidebar'; // Assurez-vous que le chemin est correct  
import Navbar from '../../components/Navbar/Navbar';  

function Add_entreprise1() {  

  return (  
    <div className="single">
    <Sidebar />
    <div className="singleContainer">
      <Navbar />{/* Ajout de la Navbar ici */}  
      <div className="map-section">  
        <h2>Ajouter Une Entreprise</h2>  
        <div className="filters">  
          <input type='text' placeholder='Search by Entreprise Number' />  
          <select>  
            <option>Commune</option>  
            {/* Ajoutez d'autres options */}  
          </select>  
          <select>  
            <option>Arrondissement</option>  
            {/* Ajoutez d'autres options */}  
          </select>  
          <button>Reset Filter</button>  
        </div>  
      
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
    </div>  
     
  );  
}  

export default Add_entreprise1;