import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';

const ProvinceComponent = () => {
  const [provinces, setProvinces] = useState([]);
  const [currentProvince, setCurrentProvince] = useState(null);
  const [provinceNom, setProvinceNom] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/province/');
        const provinces = response.data.map((province) => ({
          id: province.id_pref_prov,
          nom: province.nom,
        }));
        setProvinces(provinces);
      } catch (error) {
        console.error('Error fetching provinces:', error);
        alert('Erreur lors du chargement des provinces.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateProvince = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentProvince) {
        response = await axios.put(
          `http://localhost:8000/api/province/${currentProvince.id}/`,
          { nom: provinceNom }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/province/', { nom: provinceNom });
      }

      const updatedProvince = {
        id: response.data.id_pref_prov,
        nom: response.data.nom,
      };

      if (currentProvince) {
        setProvinces((prev) => prev.map((p) => (p.id === updatedProvince.id ? updatedProvince : p)));
      } else {
        setProvinces((prev) => [...prev, updatedProvince]);
      }

      alert(currentProvince ? 'Province modifiée avec succès!' : 'Province ajoutée avec succès!');
      resetProvinceForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteProvince = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette province ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/province/${id}/`);
        setProvinces((prev) => prev.filter((province) => province.id !== id));
        alert('Province supprimée avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditProvince = (province) => {
    setCurrentProvince(province);
    setProvinceNom(province.nom);
  };

  const resetProvinceForm = () => {
    setCurrentProvince(null);
    setProvinceNom('');
  };

  const columnsProvince = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom de la Province', flex: 1 },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="actionButton" onClick={() => handleEditProvince(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteProvince(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des provinces...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Provinces</h2>
      <form onSubmit={addOrUpdateProvince} className="formContainer">
        <div className="formInput">
          <label>Nom de la Province :</label>
          <input
            type="text"
            value={provinceNom}
            onChange={(e) => setProvinceNom(e.target.value)}
            required
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentProvince ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetProvinceForm}>
            Annuler
          </button>
        </div>
      </form>
      <Paper sx={{ height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
        <DataGrid rows={provinces} columns={columnsProvince} pageSize={5} rowsPerPageOptions={[5]} style={{ backgroundColor: '#f9f9f9' }} />
      </Paper>
    </div>
  );
};

export default ProvinceComponent;