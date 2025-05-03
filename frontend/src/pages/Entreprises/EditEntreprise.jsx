import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import './Ajouter_entreprise1.scss'; // Utiliser le même fichier SCSS que Add_entreprise1

const EditEntreprise = () => {
  const { id } = useParams(); // Récupère l'ID de l'entreprise depuis l'URL
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    id_entreprise_mere: '',
    id_commune: '',
    id_activite: '',
    nom: '',
    id_zone: '',
    lot: '',
    Ilot: '',
    avenue: '',
    rue: '',
    regime: '',
    secteur: '',
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
  const [zones, setZones] = useState([]);
  const [isTFZ, setIsTFZ] = useState(false);

  useEffect(() => {
    const loadEntrepriseData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/entreprise/${id}/`);
        const entreprise = response.data;
  
        // Pré-remplir les données de l'entreprise
        setFormData({
          id_entreprise_mere: entreprise.id_entreprise_mere,
          id_commune: entreprise.id_commune,
          id_activite: entreprise.id_activite,
          id_parcelle: entreprise.id_parcelle,
          nom: entreprise.nom,
          id_zone: entreprise.id_zone,
          lot: entreprise.lot,
          Ilot: entreprise.Ilot,
          avenue: entreprise.avenue,
          rue: entreprise.rue,
          regime: entreprise.regime,
          secteur: entreprise.secteur,
          montant_investissement: entreprise.montant_investissement,
          nombre_emploi: entreprise.nombre_emploi,
          superficie_totale: entreprise.superficie_totale,
          DAE: null, // Ne pas pré-remplir les fichiers pour éviter des problèmes de sécurité
          EIE_PSSE: null,
        });
  
        // Charger les communes en fonction de la province
        if (entreprise.id_commune_detail?.id_pref_prov) {
          setSelectedProvince(entreprise.id_commune_detail.id_pref_prov);
          const communesResponse = await axios.get(`http://localhost:8000/api/communes/?id_pref_prov=${entreprise.id_commune_detail.id_pref_prov}`);
          setCommunes(communesResponse.data);
        }
  
        // Charger les activités en fonction du secteur
        if (entreprise.id_activite_detail?.id_secteur) {
          setSelectedSecteur(entreprise.id_activite_detail.id_secteur);
          const activitesResponse = await axios.get(`http://localhost:8000/api/activites-industriellesbyid/?id_secteur=${entreprise.id_activite_detail.id_secteur}`);
          setActivites(activitesResponse.data);
        }
      } catch (error) {
        alert('Erreur lors du chargement des données de l\'entreprise');
      }
    };
  
    loadEntrepriseData();
  }, [id]);

  // Charger les listes déroulantes
  useEffect(() => {
    const loadData = async () => {
      try {
        const [entreprisesResponse, provincesResponse, secteursResponse, zonesResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/entreprise-mere/'),
          axios.get('http://localhost:8000/api/province/'),
          axios.get('http://localhost:8000/api/secteurs/'),
          axios.get('http://localhost:8000/api/zone/'),
        ]);
        setEntreprisesMeres(entreprisesResponse.data);
        setProvinces(provincesResponse.data);
        setSecteurs(secteursResponse.data);
        setZones(zonesResponse.data);
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
        const response = await axios.get(`http://localhost:8000/api/communes/?id_pref_prov=${provinceId}`);
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
        const response = await axios.get(`http://localhost:8000/api/activites-industriellesbyid/?id_secteur=${secteurId}`);
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
      setFormData((prevState) => ({
        ...prevState,
        [name]: files[0],
      }));
    } else {
      setFormData((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handleZoneChange = (e) => {
    const zoneId = e.target.value;
    setFormData((prevState) => ({
      ...prevState,
      id_zone: zoneId,
    }));

    const selectedZone = zones.find((zone) => zone.id_zone === Number(zoneId));
    setIsTFZ(selectedZone && selectedZone.nom === "TFZ");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formDataToSend = new FormData();
    for (const key in formData) {
      if (formData[key] !== null && formData[key] !== '') {
        formDataToSend.append(key, formData[key]);
      }
    }
    console.log(formData)

    console.log(formDataToSend)
    try {
      await axios.put(`http://localhost:8000/api/entreprise/${id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Entreprise modifiée avec succès!');
      navigate('/List_entreprise');
    } catch (error) {
      alert(`Erreur lors de la modification de l'entreprise: ${error.response?.data?.error || error.message}`);
    }
  };

  return (
    <div className="new">
      <Sidebar />
      <div className="newContainer">
        <Navbar />
        <div className="top">
          <h1>Modifier une entreprise</h1>
        </div>
        <div className="bottom">
          <form onSubmit={handleSubmit}>
          <h3>Informations Générales</h3>
            <div className="formSection">
              <div className="formInput">
                <label>Entreprise mère:</label>
                <select
                  name="id_entreprise_mere"
                  value={formData.id_entreprise_mere}
                  onChange={handleChange}
                  required
                >
                  <option value="" disabled>Sélectionnez une entreprise mère</option>
                  {entreprisesMeres.map((entreprise) => (
                    <option key={entreprise.id_entreprise_mere} value={entreprise.id_entreprise_mere}>
                      {entreprise.nom}
                    </option>
                  ))}
                </select>
              </div>
              <div className="formInput">
                <button className="button" type="button" onClick={() => navigate('/entreprise-mere')}>
                  Ajouter une entreprise mère
                </button>
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
                <label>Secteur dominant:</label>
                <select
                  name="secteur_dominant"
                  value={selectedSecteur}
                  onChange={handleSecteurChange}
                  required
                >
                  <option value="" disabled>Sélectionnez un secteur dominant</option>
                  {secteurs.map((secteur) => (
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
                  <option value="" disabled>Sélectionnez une activité industrielle</option>
                  {activites.map((activite) => (
                    <option key={activite.id_activite} value={activite.id_activite}>
                      {activite.nom}
                    </option>
                  ))}
                </select>
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
            </div>

            <h3>Localisation d'entreprise</h3>
            <div className="formSection">
              <div className="formInput">
                <label>Parcelle:</label>
                <input
                  type="text"
                  name="parcelle"
                  value={formData.id_parcelle}
                  readOnly
                  required
                />
              </div>
              <div className="formInput">
                <label>Zone:</label>
                <select
                  name="id_zone"
                  value={formData.id_zone}
                  onChange={handleZoneChange}
                  required
                >
                  <option value="" disabled>-- Sélectionnez une Zone --</option>
                  {zones.map((zone) => (
                    <option key={zone.id_zone} value={zone.id_zone}>
                      {zone.nom}
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
                  <option value="" disabled>Sélectionnez une province</option>
                  {provinces.map((province) => (
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
                  <option value="" disabled>Sélectionnez une commune</option>
                  {communes.map((commune) => (
                    <option key={commune.id_commune} value={commune.id_commune}>
                      {commune.nom}
                    </option>
                  ))}
                </select>
              </div>
              {isTFZ && (
                <div className="formInput">
                  <label>ILot:</label>
                  <input
                    type="text"
                    name="Ilot"
                    value={formData.Ilot}
                    onChange={handleChange}
                    required
                  />
                </div>
              )}
              <div className="formInput">
                <label>Lot:</label>
                <input
                  type="text"
                  name="lot"
                  value={formData.lot}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="formInput">
                <label>Avenue:</label>
                <input
                  type="text"
                  name="avenue"
                  value={formData.avenue}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="formInput">
                <label>Rue:</label>
                <input
                  type="text"
                  name="rue"
                  value={formData.rue}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="formInput">
                <label>Régime:</label>
                <select
                
                  name="regime"
                  value={formData.regime}
                  onChange={handleChange}
                  required
                >
                  <option value="" disabled>-- Sélectionnez un Régime --</option>
                  <option value="ZL">ZL</option>
                  <option value="ZF">ZF</option>
                </select>
              </div>
              <div className="formInput">
                <label>Secteur:</label>
                <input
                  type="text"
                  name="secteur"
                  value={formData.secteur}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <h3>Documents d'entreprise</h3>
            <div className="formSection">
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
            </div>
            <button className="button" type="submit">Modifier l'entreprise</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditEntreprise;