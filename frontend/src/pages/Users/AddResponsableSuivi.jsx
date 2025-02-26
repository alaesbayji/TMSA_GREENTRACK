import React, { useState, useEffect } from 'react';  
import { useNavigate } from 'react-router-dom';  
import axios from 'axios';  
import Sidebar from '../../components/Sidebar/Sidebar';  
import Navbar from '../../components/Navbar/Navbar';  
import './AddResponsable.scss';  
import ShowAlert from "../../components/ShowAlert";

const AddResponsableSuivi = () => {  
  const navigate = useNavigate();  

  const [zones, setZones] = useState([]);  
  const [formData, setFormData] = useState({  
    nom: '',  
    prenom: '',  
    email: '',  
    password: '',  
    role: 'ResponsableSuiviTMSA',  
    id_zone: '',  
  });  

  const [loading, setLoading] = useState(false);  

  useEffect(() => {  
    const fetchZones = async () => {  
      try {  
        const response = await axios.get('http://localhost:8000/api/zone/');  
        setZones(response.data);  
      } catch (error) {  
        ShowAlert('error', "Erreur lors du chargement des Zones disponibles.");

      }  
    };  

    fetchZones();  
  }, []);  

  const handleChange = (e) => {  
    const { name, value } = e.target;  
    setFormData((prevState) => ({  
      ...prevState,  
      [name]: value,  
    }));  
  };  

  const handleSubmit = async (e) => {  
    e.preventDefault();  
    setLoading(true);  

    try {  
       await axios.post('http://localhost:8000/api/signup/', formData, {  
        headers: {  
          'Content-Type': 'application/json',  
        },  
      });  
      ShowAlert('success', "Utilisateur créé avec succès !");
      navigate('/List_Responsable_entreprise');  
    } catch (error) {  
      ShowAlert('error', "Erreur lors du Creation d'utilisateur");
    } finally {  
      setLoading(false);  
    }  
  };  

  return (  
    <div className="newuser">  
      <Sidebar />  
      <div className="newContaineruser">  
        <Navbar />  
        <div className="topuser">  
          <h2>Ajouter un Responsable Suivi</h2>  
        </div>  
        <div className="bottomuser">  
          <form onSubmit={handleSubmit}className="formContaineruser " >  
          <div className="formRowuser">  

            <div className="formInputuser">  
              <label>Nom:</label>  
              <input  
                type="text"  
                name="nom"  
                value={formData.nom}  
                onChange={handleChange}  
                required  
              />  
            </div>  
            <div className="formInputuser">  
              <label>Prénom:</label>  
              <input  
                type="text"  
                name="prenom"  
                value={formData.prenom}  
                onChange={handleChange}  
                required  
              />  
            </div>  
            </div>  
            <div className="formRowuser">  

            <div className="formInputuser">  
              <label>Email:</label>  
              <input  
                type="email"  
                name="email"  
                value={formData.email}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInputuser">  
              <label>Mot de passe:</label>  
              <input  
                type="password"  
                name="password"  
                value={formData.password}  
                onChange={handleChange}  
                required  
              />  
            </div>  
            </div>  
            <div className="formRowuser">  

            <div className="formInputuser">  
              <label>Confirmer le mot de passe:</label>  
              <input  
                type="password"  
                // Le champ de confirmation de mot de passe est géré uniquement en frontend  
                onChange={handleChange}  
                required  
              />  
            </div>  
            <div className="formInputuser">  
              <label>Zone De Suivi</label>  
              <select  
                name="id_zone"  
                value={formData.id_zone}  
                onChange={handleChange}  
                required  
              >  
                <option value="">-- Sélectionnez une Zone --</option>  
                {zones.map((zone) => (  
                  <option key={zone.id_zone} value={zone.id_zone}>  
                    {zone.nom}  
                  </option>  
                ))}  
              </select>  
              </div>  
              </div>  
              <button type="submit" disabled={loading}>  
              {loading ? 'En cours...' : 'Ajouter le Responsable'}  
            </button>  
          </form>  
        </div>  
      </div>  
    </div>  
  );  
};  

export default AddResponsableSuivi;