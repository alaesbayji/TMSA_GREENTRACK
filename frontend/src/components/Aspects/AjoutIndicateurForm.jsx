import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import './DatatableAspect.scss';

const AjoutIndicateurForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { aspectId: initialAspectId } = location.state || {}; // Récupérer l'id_aspect depuis le state

  const [indicateurs, setIndicateurs] = useState([]);
  const [currentIndicateur, setCurrentIndicateur] = useState(null);
  const [nom, setNom] = useState('');
  const [seuilMax, setSeuilMax] = useState('');
  const [unite, setUnite] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const [aspects, setAspects] = useState([]); // État pour stocker la liste des aspects
  const [aspectId, setAspectId] = useState(initialAspectId || ''); // État pour l'aspect sélectionné

  // Charger la liste des aspects au montage du composant
  useEffect(() => {
    const fetchAspects = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/aspect/');
        // Filtrer les aspects où est_eau = False
        const filteredAspects = response.data.filter(aspect => aspect.est_eau === false);
        setAspects(filteredAspects);
      } catch (error) {
        console.error('Error fetching aspects:', error);
      }
    };

    fetchAspects();
  }, []);

  // Charger les indicateurs pour l'aspect sélectionné
  useEffect(() => {
    const fetchData = async () => {
      if (!aspectId) return; // Ne pas charger si aucun aspect n'est sélectionné

      try {
        const response = await axios.get(`http://localhost:8000/api/indicateur/?id_aspect=${aspectId}`);
        // Filtrer les indicateurs pour ne garder que ceux liés à l'id_aspect passé en props
        const filteredIndicateurs = response.data.filter(
          (indicateur) => indicateur.id_aspect === initialAspectId
        );
        setIndicateurs(filteredIndicateurs);
      } catch (error) {
        console.error('Error fetching indicateurs:', error);
        alert('Erreur lors du chargement des indicateurs.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, [aspectId, initialAspectId]); // Ajouter initialAspectId comme dépendance

  // Gérer le changement d'aspect
  const handleAspectChange = (e) => {
    const selectedAspectId = e.target.value;
    setAspectId(selectedAspectId); // Mettre à jour l'aspect sélectionné
  };

  // Ajouter ou mettre à jour un indicateur
  const addOrUpdateIndicateur = async (e) => {
    e.preventDefault();
    setLoading(true);

    const indicateurData = {
      nom,
      seuil_max: parseFloat(seuilMax),
      unite,
      id_aspect: aspectId,
    };

    try {
      let response;
      if (currentIndicateur) {
        response = await axios.put(
          `http://localhost:8000/api/indicateur/${currentIndicateur.id_indicateur}/`,
          indicateurData
        );
      } else {
        response = await axios.post('http://localhost:8000/api/indicateur/', indicateurData);
      }

      const newIndicateur = {
        id_indicateur: response.data.id_indicateur,
        nom: response.data.nom,
        seuil_max: response.data.seuil_max,
        unite: response.data.unite,
        id_aspect: response.data.id_aspect,
      };

      if (currentIndicateur) {
        setIndicateurs((prev) =>
          prev.map((i) => (i.id_indicateur === newIndicateur.id_indicateur ? newIndicateur : i))
        );
      } else {
        setIndicateurs((prev) => [...prev, newIndicateur]);
      }

      alert(currentIndicateur ? 'Indicateur modifié avec succès!' : 'Indicateur ajouté avec succès!');
      resetIndicateurForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Supprimer un indicateur
  const deleteIndicateur = async (id_indicateur) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet indicateur ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/indicateur/${id_indicateur}/`);
        setIndicateurs((prev) => prev.filter((i) => i.id_indicateur !== id_indicateur));
        alert('Indicateur supprimé avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  // Modifier un indicateur
  const handleEditIndicateur = (indicateur) => {
    setCurrentIndicateur(indicateur);
    setNom(indicateur.nom);
    setSeuilMax(indicateur.seuil_max);
    setUnite(indicateur.unite);
  };

  // Réinitialiser le formulaire
  const resetIndicateurForm = () => {
    setCurrentIndicateur(null);
    setNom('');
    setSeuilMax('');
    setUnite('');
  };

  // Colonnes pour la DataGrid
  const columnsIndicateurs = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom', flex: 1 },
    { field: 'seuil_max', headerName: 'Seuil Max', flex: 1 },
    { field: 'unite', headerName: 'Unité', flex: 1 },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="viewButton" onClick={() => handleEditIndicateur(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteIndicateur(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des indicateurs...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Indicateurs</h2>
      <div className="formInput">
        <label>Sélectionnez un aspect :</label>
        <select
          value={aspectId}
          onChange={handleAspectChange}
          required
          disabled={initialAspectId} // Désactiver si initialAspectId est défini
        >
          <option value="">Sélectionnez un aspect</option>
          {aspects.map((aspect) => (
            <option key={aspect.id_aspect} value={aspect.id_aspect}>
              {aspect.typeMilieu}
            </option>
          ))}
        </select>
      </div>

      {aspectId && (
        <>
          <form onSubmit={addOrUpdateIndicateur} className="formContainer">
            <div className="formInput">
              <label>Nom de l'indicateur :</label>
              <input
                type="text"
                value={nom}
                onChange={(e) => setNom(e.target.value)}
                required
              />
            </div>
            <div className="formInput">
              <label>Seuil maximal :</label>
              <input
                type="number"
                value={seuilMax}
                onChange={(e) => setSeuilMax(e.target.value)}
                required
              />
            </div>
            <div className="formInput">
              <label>Unité :</label>
              <input
                type="text"
                value={unite}
                onChange={(e) => setUnite(e.target.value)}
                required
              />
            </div>
            <div className="formActions">
              <button className="button" type="submit" disabled={loading}>
                {loading ? 'En cours...' : currentIndicateur ? 'Modifier' : 'Ajouter'}
              </button>
              <button className="button" type="button" onClick={resetIndicateurForm}>
                Annuler
              </button>
            </div>
          </form>

          <Paper sx={{ marginTop: '10px', height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
            <DataGrid
              rows={indicateurs.map((indicateur) => ({ ...indicateur, id: indicateur.id_indicateur }))}
              columns={columnsIndicateurs}
              pageSize={5}
              rowsPerPageOptions={[5]}
              style={{ backgroundColor: '#f9f9f9' }}
            />
          </Paper>
        </>
      )}
    </div>
  );
};

export default AjoutIndicateurForm;