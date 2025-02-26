import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import './EntrepriseMereComponents.scss'
const EntrepriseMereComponents = () => {
  const [entreprisesMere, setEntreprisesMere] = useState([]);
  const [currentEntrepriseMere, setCurrentEntrepriseMere] = useState(null);
  const [entrepriseNom, setEntrepriseNom] = useState('');
  const [statutJuridique, setStatutJuridique] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/entreprise-mere/');
        const entreprises = response.data.map((entreprise) => ({
          id: entreprise.id_entreprise_mere,
          nom: entreprise.nom,
          statut_juridique: entreprise.statut_juridique,
        }));
        setEntreprisesMere(entreprises);
      } catch (error) {
        console.error('Failed to fetch Entreprises Mères:', error);
        alert('Erreur lors du chargement des Entreprises Mères.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateEntrepriseMere = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentEntrepriseMere) {
        response = await axios.put(
          `http://localhost:8000/api/entreprise-mere/${currentEntrepriseMere.id}/`,
          {
            nom: entrepriseNom,
            statut_juridique: statutJuridique,
          }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/entreprise-mere/', {
          nom: entrepriseNom,
          statut_juridique: statutJuridique,
        });
      }

      const newEntrepriseMere = {
        id: response.data.id_entreprise_mere,
        nom: response.data.nom,
        statut_juridique: response.data.statut_juridique,
      };

      if (currentEntrepriseMere) {
        setEntreprisesMere((prev) =>
          prev.map((entreprise) => (entreprise.id === newEntrepriseMere.id ? newEntrepriseMere : entreprise))
        );
        alert('Entreprise Mère mise à jour avec succès!');
      } else {
        setEntreprisesMere((prev) => [...prev, newEntrepriseMere]);
        alert('Nouvelle Entreprise Mère ajoutée avec succès!');
      }

      resetEntrepriseForm();
    } catch (error) {
      console.error('Failed to add or update Entreprise Mère:', error);
      alert(`Erreur lors de l'opération: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteEntrepriseMere = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette Entreprise Mère ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/entreprise-mere/${id}/`);
        setEntreprisesMere((prev) => prev.filter((entreprise) => entreprise.id !== id));
        alert('Entreprise Mère supprimée avec succès!');
      } catch (error) {
        console.error('Failed to delete Entreprise Mère:', error);
        alert('Erreur lors de la suppression.');
      }
    }
  };

  const handleEditEntreprise = (entreprise) => {
    setCurrentEntrepriseMere(entreprise);
    setEntrepriseNom(entreprise.nom);
    setStatutJuridique(entreprise.statut_juridique);
  };

  const resetEntrepriseForm = () => {
    setCurrentEntrepriseMere(null);
    setEntrepriseNom('');
    setStatutJuridique('');
  };

  const columnsEntreprises = [
    { field: 'id', headerName: 'ID', flex:0.1,   },
    { field: 'nom', headerName: 'Nom',  flex:0.5   },
    { field: 'statut_juridique', headerName: 'Statut Juridique', flex:0.5 },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
    flex:1,      renderCell: (params) => (
        <>
          <button
            className="actionButton"
            onClick={() => handleEditEntreprise(params.row)}
          >
            Modifier
          </button>
          <button
            className="deleteButton"
            onClick={() => deleteEntrepriseMere(params.row.id)}
          >
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des Entreprises Mères...</div>;
  }

  return (
    <>
      <form onSubmit={addOrUpdateEntrepriseMere} className="formSection">
        <div className="formInput">
          <label>Nom :</label>
          <input
            type="text"
            value={entrepriseNom}
            onChange={(e) => setEntrepriseNom(e.target.value)}
            required
          />
        </div>
        <div className="formInput">
          <label>Statut Juridique :</label>
          <input
            type="text"
            value={statutJuridique}
            onChange={(e) => setStatutJuridique(e.target.value)}
            required
          />
        </div>
          <button  className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentEntrepriseMere ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetEntrepriseForm}>
            Annuler
          </button>
      </form>
        <Paper >
          <DataGrid rows={entreprisesMere} columns={columnsEntreprises} pageSize={5} rowsPerPageOptions={[5]} />
        </Paper>
    </>
  );
};

export default EntrepriseMereComponents;