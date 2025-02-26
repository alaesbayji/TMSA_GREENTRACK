import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../Api'; // Import the Axios instance
import ShowAlert from "../ShowAlert";
import ShowAlertConf from "../ShowAlertConf";
import './Datatable_entreprises.scss';
import BusinessIcon from '@mui/icons-material/Business';

const Datatable_entreprise = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const navigate = useNavigate();

  // Load data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('http://localhost:8000/api/entreprise/');
        
        // Ajouter une propriété `id` à chaque entreprise
        const entreprisesWithIds = response.data.map((entreprise, index) => ({
          ...entreprise,
          id: entreprise.id || index + 1,
          zone: entreprise.id_zone?.nom || 'N/A',  // Récupérer le nom de la zone
          province: entreprise.id_commune.id_pref_prov?.nom || 'N/A',  // Récupérer le nom de la zone
          commune: entreprise.id_commune?.nom || 'N/A',  // Récupérer le nom de la zone
          secteur: entreprise.id_activite.id_secteur?.nom || 'N/A',  // Récupérer le nom de la zone
        }));

        setData(entreprisesWithIds);
      } catch (error) {
        console.error('Error fetching entreprises:', error.response?.data || error.message);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, [navigate]);

  // Delete an entreprise
  const handleDelete = async (entrepriseData) => {
    const confirmed = await new Promise((resolve) => {
      ShowAlertConf(
        "warning",
        "Êtes-vous sûr de vouloir supprimer cette entreprise ?",
        {
          confirmButtonText: "Oui, Supprimer",
          cancelButtonText: "Annuler",
          showCancelButton: true,
          onConfirm: () => resolve(true),
          onCancel: () => resolve(false),
        }
      );
    });

    if (!confirmed) return;

    try {
      await api.delete(`http://127.0.0.1:8000/api/entreprise/${entrepriseData.id}/delete/`);
      setData(data.filter((item) => item.id !== entrepriseData.id));
      ShowAlert("success", "Entreprise supprimée avec succès !");
    } catch (error) {
      console.error("Error deleting data:", error.response?.data || error.message);
      ShowAlert("error", error.response?.data?.detail || "Une erreur s'est produite lors de la suppression.");
      if (error.response && error.response.status === 401) {
        navigate("/login");
      }
    }
  };

  const handleView = (entrepriseData) => {
    navigate(`/entreprises/${entrepriseData.id}`, { state: { id: entrepriseData.id } });
  };

  const columnsEntreprise = [
    { field: 'id', headerName: 'ID', flex:0.1},
    { field: 'nom', headerName: 'Nom', flex:0.2},
    { field: 'adresse', headerName: 'Adresse', flex:0.3 },
    { field: 'secteur', headerName: 'Secteur', flex:0.2},

    { field: 'zone', headerName: 'Zone', flex:0.1},
    { field: 'province', headerName: 'Province', flex:0.2},
    { field: 'commune', headerName: 'Commune', flex:0.3},
    { field: 'montant_investissement', headerName: 'Investissement', flex:0.3 },
    { field: 'nombre_emploi', headerName: 'Emplois', flex:0.2},

    {
      field: 'actions',
      headerName: 'Actions',
      flex:0.3,
      renderCell: (params) => (
        <div className="cellAction">
          <div className="viewButton" onClick={() => handleView(params.row)}>
            Consulter
          </div>
          <div className="deleteButton" onClick={() => handleDelete(params.row)}>
            Supprimer
          </div>
        </div>
      ),
    },
  ];

  if (isFetching) {
    return <div>Chargement des entreprises...</div>;
  }

  return (
    <div className="datatable">
      <div className="datatableTitle" style={{ color: '#00A2DD' }}>
        Gestion des Entreprises
        <Link to="/ajouter_entreprise1" className="link">
          <BusinessIcon /> Ajouter une nouvelle entreprise
        </Link>
      </div>
      <DataGrid
        className="datagrid"
        rows={data}
        columns={columnsEntreprise}
        pageSize={9}
        rowsPerPageOptions={[9]}
        checkboxSelection
        getRowId={(row) => row.id} // Utiliser la propriété `id` comme clé unique
      />
    </div>
  );
};

export default Datatable_entreprise;