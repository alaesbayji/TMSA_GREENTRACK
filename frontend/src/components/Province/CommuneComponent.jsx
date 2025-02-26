import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';

const CommuneComponent = () => {
  const [communes, setCommunes] = useState([]);
  const [currentCommune, setCurrentCommune] = useState(null);
  const [communeNom, setCommuneNom] = useState('');
  const [provinceId, setProvinceId] = useState('');
  const [provinces, setProvinces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [communeResponse, provinceResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/commune/'),
          axios.get('http://localhost:8000/api/province/'),
        ]);

        const communes = communeResponse.data.map((commune) => ({
          id: commune.id_commune,
          nom: commune.nom,
          province: provinceResponse.data.find((p) => p.id_pref_prov === commune.id_pref_prov) || null,
        }));

        setCommunes(communes);
        setProvinces(provinceResponse.data);
      } catch (error) {
        console.error('Error fetching communes:', error);
        alert('Erreur lors du chargement des communes.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateCommune = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentCommune) {
        response = await axios.put(
          `http://localhost:8000/api/commune/${currentCommune.id}/`,
          { nom: communeNom, id_pref_prov: provinceId }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/commune/', {
          nom: communeNom,
          id_pref_prov: provinceId,
        });
      }

      const newCommune = {
        id: response.data.id_commune,
        nom: response.data.nom,
        province: provinces.find((p) => p.id_pref_prov === parseInt(provinceId)) || null,
      };

      if (currentCommune) {
        setCommunes((prev) => prev.map((c) => (c.id === newCommune.id ? newCommune : c)));
      } else {
        setCommunes((prev) => [...prev, newCommune]);
      }

      alert(currentCommune ? 'Commune modifiée avec succès!' : 'Commune ajoutée avec succès!');
      resetCommuneForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteCommune = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette commune ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/commune/${id}/`);
        setCommunes((prev) => prev.filter((commune) => commune.id !== id));
        alert('Commune supprimée avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditCommune = (commune) => {
    setCurrentCommune(commune);
    setCommuneNom(commune.nom);
    setProvinceId(commune.province?.id_pref_prov || '');
  };

  const resetCommuneForm = () => {
    setCurrentCommune(null);
    setCommuneNom('');
    setProvinceId('');
  };

  const columnsCommune = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom de la Commune', flex: 1 },
    {
      field: 'province',
      headerName: 'Province',
      flex: 1,
      renderCell: (params) => params.row.province?.nom || 'N/A',
    },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="actionButton" onClick={() => handleEditCommune(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteCommune(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des communes...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Communes</h2>
      <form onSubmit={addOrUpdateCommune} className="formContainer">
        <div className="formInput">
          <label>Province :</label>
          <select
            name="id_pref_prov"
            value={provinceId}
            onChange={(e) => setProvinceId(e.target.value)}
            required
          >
            <option value="" disabled>
              Sélectionnez une province
            </option>
            {provinces.map((province) => (
              <option key={province.id_pref_prov} value={province.id_pref_prov}>
                {province.nom}
              </option>
            ))}
          </select>
        </div>
        <div className="formInput">
          <label>Nom de la Commune :</label>
          <input
            type="text"
            value={communeNom}
            onChange={(e) => setCommuneNom(e.target.value)}
            required
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentCommune ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetCommuneForm}>
            Annuler
          </button>
        </div>
      </form>
      <Paper sx={{ height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
        <DataGrid rows={communes} columns={columnsCommune} pageSize={5} rowsPerPageOptions={[5]} style={{ backgroundColor: '#f9f9f9' }} />
      </Paper>
    </div>
  );
};

export default CommuneComponent;