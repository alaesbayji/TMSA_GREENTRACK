import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';

const SecteurComponent = () => {
  const [secteurs, setSecteurs] = useState([]);
  const [currentSecteur, setCurrentSecteur] = useState(null);
  const [secteurNom, setSecteurNom] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/secteurs/');
        const secteurs = response.data.map((secteur) => ({
          id: secteur.id_secteur,
          nom: secteur.nom,
        }));
        setSecteurs(secteurs);
      } catch (error) {
        console.error('Error fetching secteurs:', error);
        alert('Erreur lors du chargement des secteurs.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateSecteur = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentSecteur) {
        response = await axios.put(
          `http://localhost:8000/api/secteurs/${currentSecteur.id}/`,
          { nom: secteurNom }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/secteurs/', { nom: secteurNom });
      }

      const updatedSecteur = {
        id: response.data.id_secteur,
        nom: response.data.nom,
      };

      if (currentSecteur) {
        setSecteurs((prev) => prev.map((s) => (s.id === updatedSecteur.id ? updatedSecteur : s)));
      } else {
        setSecteurs((prev) => [...prev, updatedSecteur]);
      }

      alert(currentSecteur ? 'Secteur modifié avec succès!' : 'Secteur ajouté avec succès!');
      resetSecteurForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteSecteur = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce secteur ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/secteurs/${id}/`);
        setSecteurs((prev) => prev.filter((secteur) => secteur.id !== id));
        alert('Secteur supprimé avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditSecteur = (secteur) => {
    setCurrentSecteur(secteur);
    setSecteurNom(secteur.nom);
  };

  const resetSecteurForm = () => {
    setCurrentSecteur(null);
    setSecteurNom('');
  };

  const columnsSecteurs = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom du Secteur', flex: 1 },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="actionButton" onClick={() => handleEditSecteur(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteSecteur(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des secteurs...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Secteurs</h2>
      <form onSubmit={addOrUpdateSecteur} className="formContainer">
        <div className="formInput">
          <label>Nom du Secteur :</label>
          <input
            type="text"
            value={secteurNom}
            onChange={(e) => setSecteurNom(e.target.value)}
            required
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentSecteur ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetSecteurForm}>
            Annuler
          </button>
        </div>
      </form>
      <Paper sx={{ height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
        <DataGrid rows={secteurs} columns={columnsSecteurs} pageSize={5} rowsPerPageOptions={[5]} style={{ backgroundColor: '#f9f9f9' }} />
      </Paper>
    </div>
  );
};

export default SecteurComponent;