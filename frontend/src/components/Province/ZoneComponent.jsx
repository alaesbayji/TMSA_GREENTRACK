import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';

const ZoneComponent = () => {
  const [zones, setZones] = useState([]);
  const [currentZone, setCurrentZone] = useState(null);
  const [zoneNom, setZoneNom] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/zone/');
        const zones = response.data.map((zone) => ({
          id: zone.id_zone,
          nom: zone.nom,
        }));
        setZones(zones);
      } catch (error) {
        console.error('Error fetching zones:', error);
        alert('Erreur lors du chargement des zones.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateZone = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (currentZone) {
        response = await axios.put(
          `http://localhost:8000/api/zone/${currentZone.id}/`,
          { nom: zoneNom }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/zone/', { nom: zoneNom });
      }

      const newZone = {
        id: response.data.id_zone,
        nom: response.data.nom,
      };

      if (currentZone) {
        setZones((prev) => prev.map((z) => (z.id === newZone.id ? newZone : z)));
      } else {
        setZones((prev) => [...prev, newZone]);
      }

      alert(currentZone ? 'Zone modifiée avec succès!' : 'Zone ajoutée avec succès!');
      resetZoneForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteZone = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette zone ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/zone/${id}/`);
        setZones((prev) => prev.filter((zone) => zone.id !== id));
        alert('Zone supprimée avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditZone = (zone) => {
    setCurrentZone(zone);
    setZoneNom(zone.nom);
  };

  const resetZoneForm = () => {
    setCurrentZone(null);
    setZoneNom('');
  };

  const columnsZone = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom de la Zone', flex: 1 },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
          <button className="actionButton" onClick={() => handleEditZone(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteZone(params.row.id)}>
            Supprimer
          </button>
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des zones...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Zones</h2>
      <form onSubmit={addOrUpdateZone} className="formContainer">
        <div className="formInput">
          <label>Nom de la Zone :</label>
          <input
            type="text"
            value={zoneNom}
            onChange={(e) => setZoneNom(e.target.value)}
            required
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentZone ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetZoneForm}>
            Annuler
          </button>
        </div>
      </form>
      <Paper sx={{ height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
        <DataGrid rows={zones} columns={columnsZone} pageSize={5} rowsPerPageOptions={[5]} style={{ backgroundColor: '#f9f9f9' }} />
      </Paper>
    </div>
  );
};

export default ZoneComponent;