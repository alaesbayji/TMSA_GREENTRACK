import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import './AddResponsable.scss';
import ShowAlert from "../../components/ShowAlert";
import api from '../../Api'; // Import the Axios instance

const EditResponsableSuivi = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Récupère l'ID du responsable depuis l'URL
  const [confirmPassword, setConfirmPassword] = useState(''); // New state for confirmation password  

  const [zones, setZones] = useState([]);  
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    email: '',
    password: '',
    role: 'ResponsableSuiviTMSA',
    id_entreprise: '',
  });

  const [loading, setLoading] = useState(false);

  // Récupérer les données du responsable existant
  useEffect(() => {
    const fetchResponsable = async () => {
      try {
        const response = await api.get(`http://localhost:8000/api/responsables-suivi/${id}/`);
        const responsable = response.data;
        setFormData({
          nom: responsable.nom,
          prenom: responsable.prenom,
          email: responsable.email,
          password: '', // Le mot de passe n'est pas pré-rempli pour des raisons de sécurité
          role: 'ResponsableSuiviTMSA',  
          id_zone: responsable.id_zone,
        });
      } catch (error) {
        ShowAlert('error', "Erreur lors du chargement des données du responsable.");
      }
    };

    fetchResponsable();
  }, [id]);

  // Récupérer la liste des entreprises
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
    if (name === 'confirm_password') {  
        setConfirmPassword(value); // Update confirm password separately  
      } else {  
        setFormData((prevState) => ({  
          ...prevState,  
          [name]: value,  
        }));  
      }  
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log(formData)
    if (formData.password !== confirmPassword) {  
        ShowAlert('error', "Les mots de passe ne correspondent pas.");  
        setLoading(false);  
        return;  
      }  
    try {
      await api.put(`http://localhost:8000/api/responsables-suivi/${id}/update/`, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      ShowAlert('success', "Responsable de suivi modifié avec succès !");
      navigate('/List_Responsable_suivi');
    } catch (error) {
      ShowAlert('error', "Erreur lors de la modification du responsable.");
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
          <h2>Modifier un Responsable d'Entreprise</h2>
        </div>
        <div className="bottomuser">
          <form onSubmit={handleSubmit} className="formContaineruser">
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
                  placeholder="Laissez vide pour ne pas modifier"
                />
              </div>
            </div>
            <div className="formRowuser">
            <div className="formInputuser">  
                <label>Confirmer le mot de passe:</label>  
                <input  
                  type="password"  
                  name="confirm_password"  
                  value={confirmPassword} // Use the separate state  
                  onChange={handleChange}  
                  placeholder="Confirmez le mot de passe"  
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
              {loading ? 'En cours...' : 'Modifier le Responsable'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditResponsableSuivi;