import React, { useState, useEffect } from 'react';  
import { useLocation, useNavigate } from 'react-router-dom';  
import axios from 'axios';  
import Sidebar from '../../components/Sidebar/Sidebar';  
import Navbar from '../../components/Navbar/Navbar';  
import './add_Entreprise.css'; // Inclure le style approprié  

const Add_entreprise2 = () => {  
  const location = useLocation();  
  const { id_parcelle } = location.state || {}; // Récupérer l'id_parcelle  
  const navigate = useNavigate(); // Pour la navigation  

  const [formData, setFormData] = useState({  
    id_entreprise_mere: '',  
    id_commune: '',  
    id_activite: '',  
    nom: '',  
    adresse: '',  
    zone: '',  
    montant_investissement: 0,  
    nombre_emploi: 0,  
    superficie_totale: 0,  
    DAE: null,  
    EIE_PSSE: null,  
  });  

  const [entreprisesMeres, setEntreprisesMeres] = useState([]);  
  const [provinces, setProvinces] = useState([]);  
  const [communes, setCommunes] = useState([]);  
  const [selectedProvince, setSelectedProvince] = useState('');  
  const [secteurs, setSecteurs] = useState([]);  
  const [activites, setActivites] = useState([]);  
  const [selectedSecteur, setSelectedSecteur] = useState('');  

  useEffect(() => {  
    const loadData = async () => {  
      try {  
        const [entreprisesResponse, provincesResponse, secteursResponse] = await Promise.all([  
          axios.get('http://localhost:8000/api/entreprise-mere/'),  
          axios.get('http://localhost:8000/api/province/'),  
          axios.get('http://localhost:8000/api/secteurs/')  
        ]);  
        setEntreprisesMeres(entreprisesResponse.data);  
        setProvinces(provincesResponse.data);  
        setSecteurs(secteursResponse.data);  
      } catch (error) {  
        alert('Erreur lors du chargement des données');  
      }  
    };  

    loadData();  
  }, []);  

  const handleProvinceChange = async (e) => {  
    const provinceId = e.target.value;  
    setSelectedProvince(provinceId);  

    if (provinceId) {  
      try {  
        const response = await axios.get(`http://localhost:8000/api/commune/?id_pref_prov=${provinceId}`);  
        setCommunes(response.data);  
      } catch (error) {  
        alert('Erreur lors du chargement des communes');  
      }  
    } else {  
      setCommunes([]);  
    }  
  };  

  const handleSecteurChange = async (e) => {  
    const secteurId = e.target.value;  
    setSelectedSecteur(secteurId);  

    if (secteurId) {  
      try {  
        const response = await axios.get(`http://localhost:8000/api/activites-industrielles/?id_secteur=${secteurId}`);  
        setActivites(response.data);  
      } catch (error) {  
        alert('Erreur lors du chargement des activités');  
      }  
    } else {  
      setActivites([]);  
    }  
  };  

  const handleChange = (e) => {  
    const { name, value, files } = e.target;  
  
    if (files) {  
      setFormData(prevState => ({  
        ...prevState,  
        [name]: files[0]  
      }));  
    } else {  
      setFormData(prevState => ({  
        ...prevState,  
        [name]: value  
      }));  
    }  
  };  

  const handleSubmit = async (e) => {  
    e.preventDefault();  
  
    const formDataToSend = new FormData();  
    for (const key in formData) {  
      if (formData[key] !== null) {  
        formDataToSend.append(key, formData[key]);  
      }  
    }  
    formDataToSend.append('id_parcelle', id_parcelle);  
  
    try {  
      await axios.post('http://localhost:8000/api/entreprise/', formDataToSend, {  
        headers: {  
          'Content-Type': 'multipart/form-data'  
        }  
      });  
      alert('Entreprise ajoutée avec succès!');  
      navigate('/ajouter_entreprise1');  
    } catch (error) {  
      alert(`Erreur lors de l'ajout de l'entreprise: ${error.response?.data?.error || error.message}`);  
    }  
  };  

  return (  
    <div className="new">  
      <Sidebar />  
      <div className="newContainer">  
        <Navbar />  
        <div className="top">  
          <h2>Ajouter une entreprise</h2>  
        </div>  
        <div className="bottom">  
          <form onSubmit={handleSubmit}>  
            <div className="formInput">  
            <label>Parcelle </label> 
            <input  
                type="text"  
                name="parcelle"  
                value={id_parcelle}
                required 
                readonly   
              />   </div>
                         <div className="formInput">  

              <label>Entreprise mère:</label>  
              <select  
                name="id_entreprise_mere"  
                value={formData.id_entreprise_mere}  
                onChange={handleChange}  
                required  
              >  
                <option value="">Sélectionnez une entreprise mère</option>  
                {entreprisesMeres.map(entreprise => (  
                  <option key={entreprise.id_entreprise_mere} value={entreprise.id_entreprise_mere}>  
                    {entreprise.nom}  
                  </option>  
                ))}  
              </select>  
            </div>  

            <div className="formInput">  
              <label>Province:</label>  
              <select  
                name="id_pref_prov"  
                value={selectedProvince}  
                onChange={handleProvinceChange}  
                required  
              >  
                <option value="">Sélectionnez une province</option>  
                {provinces.map(province => (  
                  <option key={province.id_pref_prov} value={province.id_pref_prov}>  
                    {province.nom}  
                  </option>  
                ))}  
              </select>  
            </div>  

            <div className="formInput">  
              <label>Communes:</label>  
              <select  
                name="id_commune"  
                value={formData.id_commune}  
                onChange={handleChange}  
                required  
              >  
                <option value="">Sélectionnez une commune</option>  
                {communes.map(commune => (  
                  <option key={commune.id_commune} value={commune.id_commune}>  
                    {commune.nom}  
                  </option>  
                ))}  
              </select>  
            </div>  

            <div className="formInput">  
              <label>Secteur dominant:</label>  
              <select  
                name="secteur_dominant"  
                value={selectedSecteur}  
                onChange={handleSecteurChange}  
                required  
              >  
                <option value="">Sélectionnez un secteur dominant</option>  
                {secteurs.map(secteur => (  
                  <option key={secteur.id_secteur} value={secteur.id_secteur}>  
                    {secteur.nom}  
                  </option>  
                ))}  
              </select>  
            </div>  

            <div className="formInput">  
              <label>Activité industrielle:</label>  
              <select  
                name="id_activite"  
                value={formData.id_activite}  
                onChange={handleChange}  
                required  
              >  
                <option value="">Sélectionnez une activité industrielle</option>  
                {activites.map(activite => (  
                  <option key={activite.id_activite} value={activite.id_activite}>  
                    {activite.nom}  
                  </option>  
                ))}  
              </select>  
            </div>  

            <div className="formInput">  
              <label>Nom de l'entreprise:</label>  
              <input  
                type="text"  
                name="nom"  
                value={formData.nom}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>Adresse:</label>  
              <input  
                type="text"  
                name="adresse"  
                value={formData.adresse}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>Zone:</label>  
              <input  
                type="text"  
                name="zone"  
                value={formData.zone}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>Montant d'investissement:</label>  
              <input  
                type="number"  
                name="montant_investissement"  
                value={formData.montant_investissement}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>Nombre d'emplois:</label>  
              <input  
                type="number"  
                name="nombre_emploi"  
                value={formData.nombre_emploi}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>Superficie totale (m²):</label>  
              <input  
                type="number"  
                name="superficie_totale"  
                value={formData.superficie_totale}  
                onChange={handleChange}  
                required  
              />  
            </div>  

            <div className="formInput">  
              <label>DAE (Fichier):</label>  
              <input  
                type="file"  
                name="DAE"  
                onChange={handleChange}  
              />  
            </div>  

            <div className="formInput">  
              <label>EIE/PSSE (Fichier):</label>  
              <input  
                type="file"  
                name="EIE_PSSE"  
                onChange={handleChange}  
              />  
            </div>  
            <button type="submit">Ajouter l'entreprise</button>  
          </form>  
        </div>  
      </div>  
    </div>  
  );  
};  

export default Add_entreprise2;