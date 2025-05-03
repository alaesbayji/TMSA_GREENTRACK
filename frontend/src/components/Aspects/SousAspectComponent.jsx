import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import './DatatableAspect.scss';
import { Link, useNavigate } from 'react-router-dom';

const SousAspectComponent = () => {
  const location = useLocation();
  const aspectIdFromState = location.state?.aspectId; // Récupérer l'id_aspect depuis le state
  const [sousAspects, setSousAspects] = useState([]);
  const [aspects, setAspects] = useState([]);
  const [currentSousAspect, setCurrentSousAspect] = useState(null);
  const [nom, setNom] = useState('');
  const [estPollution, setEstPollution] = useState(false);
  const [selectedAspectId, setSelectedAspectId] = useState(aspectIdFromState || '');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const navigate = useNavigate();

  // Charger les sous-aspects et les aspects
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sousAspectsResponse, aspectsResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/sous-aspects-eau-pollution/'),
          axios.get('http://localhost:8000/api/aspect/')
        ]);

        setSousAspects(sousAspectsResponse.data);
        setAspects(aspectsResponse.data.filter(a => a.est_eau)); // Filtrer les aspects avec est_eau=true
      } catch (error) {
        console.error('Error fetching data:', error);
        alert('Erreur lors du chargement des données');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateSousAspect = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const sousAspectData = {
        nom,
        est_pollution: estPollution,
        aspect: selectedAspectId
      };

      let response;
      if (currentSousAspect) {
        response = await axios.put(
          `http://localhost:8000/api/sous-aspects-eau-pollution/${currentSousAspect.id_sous_aspect}/`,
          sousAspectData
        );
      } else {
        response = await axios.post(
          'http://localhost:8000/api/sous-aspects-eau-pollution/',
          sousAspectData
        );
      }

      const newSousAspect = {
        id_sous_aspect: response.data.id_sous_aspect,
        nom: response.data.nom,
        est_pollution: response.data.est_pollution,
        aspect: aspects.find(a => a.id_aspect === response.data.aspect) || null
      };

      if (currentSousAspect) {
        setSousAspects(prev => prev.map(sa => sa.id_sous_aspect === newSousAspect.id_sous_aspect ? newSousAspect : sa));
      } else {
        setSousAspects(prev => [...prev, newSousAspect]);
      }

      resetForm();
      alert(currentSousAspect ? 'Sous-aspect modifié !' : 'Sous-aspect ajouté !');
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteSousAspect = async (id_sous_aspect) => {
    if (window.confirm('Confirmer la suppression ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/sous-aspects-eau-pollution/${id_sous_aspect}/`);
        setSousAspects(prev => prev.filter(sa => sa.id_sous_aspect !== id_sous_aspect));
        alert('Supprimé avec succès !');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEdit = (sousAspect) => {
    setCurrentSousAspect(sousAspect);
    setNom(sousAspect.nom);
    setEstPollution(sousAspect.est_pollution);
    setSelectedAspectId(sousAspect.aspect?.id_aspect || '');
  };

  const resetForm = () => {
    setCurrentSousAspect(null);
    setNom('');
    setEstPollution(false);
    setSelectedAspectId(aspectIdFromState || ''); // Réinitialiser avec l'id_aspect passé
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nom', headerName: 'Nom', flex: 1 },
    { 
      field: 'est_pollution', 
      headerName: 'Pollution', 
      flex: 1,
      renderCell: (params) => params.value ? 'Oui' : 'Non'
    },
    { 
      field: 'aspect', 
      headerName: 'Aspect lié', 
      flex: 1,
      renderCell: (params) => params.row.aspect?.typeMilieu || 'N/A'
    },
    {
      field: 'actions',
      headerName: 'Actions',
      flex: 1,
      renderCell: (params) => (
        <div>
           {!params.row.est_pollution && ( // Conditionally render the third button
           <button
           className="addButton"
           onClick={() => navigate('/indicateursousaspect', { state: { sousAspectId: params.row.id } })} // Passer l'id_aspect dans le state
         >
           Ajouter Indicateur
         </button>
          )}
           {params.row.est_pollution && ( // Conditionally render the third button
           <button
           className="addButton"
           onClick={() => navigate('/indicateurpollution', { state: { sousAspectId: params.row.id } })} // Passer l'id_aspect dans le state
         >
           Ajouter Indicateur
         </button>
          )}
          <button className="viewButton" onClick={() => handleEdit(params.row)}>Modifier</button>
          <button className="deleteButton" onClick={() => deleteSousAspect(params.row.id)}>Supprimer</button>
          
        </div>
      )
    }
  ];

  if (isFetching) return <div>Chargement...</div>;

  return (
    <div className="formSection">
      <h2>Gestion des Sous-Aspects Eau/Pollution</h2>
      
      <form onSubmit={addOrUpdateSousAspect} className="formContainer">
        <div className="formInput">
          <label>Nom :</label>
          <input
            type="text"
            value={nom}
            onChange={(e) => setNom(e.target.value)}
            required
          />
        </div>

        <div className="formInputs">
          <label>Pollution :</label>
          <input  style={{width:'20px',height:'20px'}}
            type="checkbox"
            checked={estPollution}
            onChange={(e) => setEstPollution(e.target.checked)}
          />
        </div>

        <div className="formInput">
          <label>Aspect lié :</label>
          <select
            value={selectedAspectId}
            onChange={(e) => setSelectedAspectId(e.target.value)}
            required
          >
            <option value="">Sélectionnez un aspect</option>
            {aspects.map(aspect => (
              <option key={aspect.id_aspect} value={aspect.id_aspect}>
                {aspect.typeMilieu}
              </option>
            ))}
          </select>
        </div>

        <div className="formActions">
          <button className='button' type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentSousAspect ? 'Modifier' : 'Ajouter'}
          </button>
          <button className='button' type="button" onClick={resetForm}>Annuler</button>
        </div>
      </form>

      <Paper style={{ marginTop: 20, height: 400 }}>  
        <DataGrid
          rows={sousAspects.map(sousAspect => ({
            id: sousAspect.id_sous_aspect,
            nom: sousAspect.nom,
            est_pollution: sousAspect.est_pollution,
            aspect: aspects.find(a => a.id_aspect === sousAspect.aspect) || null
          }))}   
          columns={columns}
          pageSize={5}
          rowsPerPageOptions={[5]}
        />  
      </Paper>  
    </div>
  );
};

export default SousAspectComponent;

