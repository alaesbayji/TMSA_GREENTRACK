import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './DatatableAspect.scss';

const AspectComponent = () => {
  const [aspects, setAspects] = useState([]);
  const [currentAspect, setCurrentAspect] = useState(null);
  const [typeMilieu, setTypeMilieu] = useState('');
  const [description, setDescription] = useState('');
  const [estEau, setEstEau] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/aspect/');
        setAspects(response.data);
      } catch (error) {
        console.error('Error fetching aspects:', error);
        alert('Erreur lors du chargement des aspects.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  const addOrUpdateAspect = async (e) => {
    e.preventDefault();
    setLoading(true);
  
    try {
      let response;
      if (currentAspect) {
        response = await axios.put(
          `http://localhost:8000/api/aspect/${currentAspect.id_aspect}/`, // Utilisez id_aspect ici
          { typeMilieu, description, est_eau: estEau }
        );
      } else {
        response = await axios.post('http://localhost:8000/api/aspect/', {
          typeMilieu,
          description,
          est_eau: estEau,
        });
      }
  
      const newAspect = {
        id_aspect: response.data.id_aspect, // Utilisez id_aspect ici
        typeMilieu: response.data.typeMilieu,
        description: response.data.description,
        est_eau: response.data.est_eau,
      };
  
      if (currentAspect) {
        setAspects((prev) => prev.map((a) => (a.id_aspect === newAspect.id_aspect ? newAspect : a))); // Utilisez id_aspect ici
      } else {
        setAspects((prev) => [...prev, newAspect]);
      }
  
      alert(currentAspect ? 'Aspect modifié avec succès!' : 'Aspect ajouté avec succès!');
      resetAspectForm();
    } catch (error) {
      console.error('Error:', error);
      alert(`Erreur lors de l'ajout ou de la modification: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteAspect = async (id_aspect) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet aspect ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/aspect/${id_aspect}/`);
        setAspects((prev) => prev.filter((aspect) => aspect.id_aspect !== id_aspect)); // Utilisez id_aspect ici
        alert('Aspect supprimé avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  const handleEditAspect = (aspect) => {
    setCurrentAspect(aspect);
    setTypeMilieu(aspect.typeMilieu);
    setDescription(aspect.description);
    setEstEau(aspect.est_eau);
  };

  const resetAspectForm = () => {
    setCurrentAspect(null);
    setTypeMilieu('');
    setDescription('');
    setEstEau(false);
  };

  const columnsAspects = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'typeMilieu', headerName: 'Type de milieu', flex: 0.5 },
    { field: 'description', headerName: 'Description', flex: 0.5},
    {
      field: 'est_eau',
      headerName: 'Concerne l\'eau',
      flex: 0.5,
      renderCell: (params) => (params.row.est_eau ? 'Oui' : 'Non'),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      flex: 1,
      renderCell: (params) => (
        <>
           {params.row.est_eau && ( // Conditionally render the third button
           <button
           className="addButton"
           onClick={() => navigate('/sous_aspect', { state: { aspectId: params.row.id_aspect } })} // Passer l'id_aspect dans le state
         >
           Ajouter Sous-aspect
         </button>
          )}
           {!params.row.est_eau && ( // Conditionally render the third button
           <button
           className="addButton"
           onClick={() => navigate('/indicateur', { state: { aspectId: params.row.id_aspect } })} // Passer l'id_aspect dans le state
         >
           Ajouter Indicateur
         </button>
          )}
          <button className="viewButton" onClick={() => handleEditAspect(params.row)}>
            Modifier
          </button>
          <button className="deleteButton" onClick={() => deleteAspect(params.row.id)}>
            Supprimer
          </button>
       
        </>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des aspects...</div>;
  }

  return (
    <div className="formSection">
      <h2>Gestion des Aspects environnementaux</h2>
      <form onSubmit={addOrUpdateAspect} className="formContainer">
        <div className="formInput">
          <label>Type de milieu :</label>
          <input
            type="text"
            value={typeMilieu}
            onChange={(e) => setTypeMilieu(e.target.value)}
            required
          />
        </div>
        <div className="formInput">
          <label>Description :</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className="formInputs">
          <label>Concerne l'eau :</label>
          <input
            type="checkbox"
            checked={estEau}
            onChange={(e) => setEstEau(e.target.checked)}
          />
        </div>
        <div className="formActions">
          <button className="button" type="submit" disabled={loading}>
            {loading ? 'En cours...' : currentAspect ? 'Modifier' : 'Ajouter'}
          </button>
          <button className="button" type="button" onClick={resetAspectForm}>
            Annuler
          </button>
        </div>
      </form>
<Paper sx={{ marginTop: '10px', height: 'auto', width: '100%', '& .MuiDataGrid-columnHeader': { backgroundColor: '#f9f9f9' } }}>
  <DataGrid
    rows={aspects.map((aspect) => ({ ...aspect, id: aspect.id_aspect }))} // Map id_aspect to id
    columns={columnsAspects}
    pageSize={5}
    rowsPerPageOptions={[5]}
    style={{ backgroundColor: '#f9f9f9' }}
  />
</Paper>
    </div>
  );
};

export default AspectComponent;