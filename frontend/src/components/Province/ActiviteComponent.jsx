import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';

const ActiviteComponent = () => {
  const [activites, setActivites] = useState([]);
  const [currentActivite, setCurrentActivite] = useState(null);
  const [activiteNom, setActiviteNom] = useState('');
  const [secteurId, setSecteurId] = useState('');
  const [secteurs, setSecteurs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [activiteResponse, secteurResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/activites-industrielles/'),
          axios.get('http://localhost:8000/api/secteurs/'),
        ]);

        const activites = activiteResponse.data.map((activite) => ({
          id: activite.id_activite,
          nom: activite.nom,
          secteur: secteurResponse.data.find((s) => s.id_secteur === activite.id_secteur) || null,
        }));

        setActivites(activites);
        setSecteurs(secteurResponse.data);
      } catch (error) {
        console.error('Error fetching activites:', error);
        alert('Erreur lors du chargement des activités.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateActivite = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentActivite) {
        response = await axios.put(
          `http://localhost:8000/api/activites-industrielles/${currentActivite.id}/`,
          { nom: activiteNom, id_secteur: secteurId }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/activites-industrielles/', {
          nom: activiteNom,
          id_secteur: secteurId,
        });
      }

      const newActivite = {
        id: response.data.id_activite,
        nom: response.data.nom,
        secteur: secteurs.find((s) => s.id_secteur === parseInt(secteurId)) || null,
      };

      if (currentActivite) {
        setActivites((prev) => prev.map((a) => (a.id === newActivite.id ? newActivite : a)));
      } else {
        setActivites((prev) => [...prev, newActivite]);
      }

      alert(currentActivite ? 'Activité modifiée avec succès!' : 'Activité ajoutée avec succès!');
      resetActiviteForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteActivite = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette activité ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/activites-industrielles/${id}/`);
        setActivites((prev) => prev.filter((activite) => activite.id !== id));
        alert('Activité supprimée avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditActivite = (activite) => {
    setCurrentActivite(activite);
    setActiviteNom(activite.nom);
    setSecteurId(activite.secteur ? activite.secteur.id_secteur : '');
  };

  const resetActiviteForm = () => {
    setCurrentActivite(null);
    setActiviteNom('');
    setSecteurId('');
  };

  const columnsActivites = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom de l\'activité', flex: 1 },
    {
      field: 'secteur',
      headerName: 'Secteur',
      flex: 1,
      renderCell: (params) => params.row.secteur?.nom || 'N/A',
    },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="actionButton" onClick={() => handleEditActivite(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteActivite(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des activités...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Activités industrielles</h2>
      <form onSubmit={addOrUpdateActivite} className="formContainer">
        <div className="formInput">
          <label>Secteur :</label>
          <select
            name="id_secteur"
            value={secteurId}
            onChange={(e) => setSecteurId(e.target.value)}
            required
          >
            <option value="" disabled>
              Sélectionnez un Secteur
            </option>
            {secteurs.map((secteur) => (
              <option key={secteur.id_secteur} value={secteur.id_secteur}>
                {secteur.nom}
              </option>
            ))}
          </select>
        </div>
        <div className="formInput">
          <label>Nom de l'activité :</label>
          <input
            type="text"
            value={activiteNom}
            onChange={(e) => setActiviteNom(e.target.value)}
            required
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentActivite ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetActiviteForm}>
            Annuler
          </button>
        </div>
      </form>
      <Paper sx={{ height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
        <DataGrid rows={activites} columns={columnsActivites} pageSize={5} rowsPerPageOptions={[5]} style={{ backgroundColor: '#f9f9f9' }} />
      </Paper>
    </div>
  );
};

export default ActiviteComponent;