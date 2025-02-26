import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../Api'; // Import the Axios instance
import ShowAlert from "../ShowAlert";
import ShowAlertConf from "../ShowAlertConf";
import './Datatable_users.scss';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
const Datatable_suivi = () => {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  // Load data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('http://localhost:8000/api/responsables-suivi/');
        // Ajouter un champ `id` temporaire si nécessaire
        const dataWithIds = response.data.map((item, index) => ({
          ...item,
          id: item.idUtilisateur || index,
          zone: item.id_zone?.nom || 'N/A',  // Récupérer le nom de la zone
          // Utilisez `idUtilisateur` ou un index comme clé
        }));
        setData(dataWithIds);
      } catch (error) {
        console.error('Error fetching data:', error.response?.data || error.message);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      }
    };
    fetchData();
  }, [navigate]);

  // Delete a user
  const handleDelete = async (userData) => {
    const confirmed = await new Promise((resolve) => {
      ShowAlertConf(
        "warning",
        "Êtes-vous sûr de vouloir supprimer cet utilisateur ?",
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
      await api.delete(`http://127.0.0.1:8000/api/responsables-suivi/${userData.id}/delete/`);
      setData(data.filter((item) => item.id !== userData.id));
      ShowAlert("success", "Responsable d'entreprise supprimé avec succès !");
    } catch (error) {
      console.error("Error deleting data:", error.response?.data || error.message);
      ShowAlert("error", error.response?.data?.detail || "Une erreur s'est produite lors de la suppression.");
      if (error.response && error.response.status === 401) {
        navigate("/login");
      }
    }
  };

  const handleView = (userData) => {
    navigate(`/users/${userData.id}`, { state: { id: userData.id } });
  };

  const userColumns = [
    { field: 'nom', headerName: 'Nom', width: 150 },
    { field: 'prenom', headerName: 'Prénom', width: 150 },
    { field: 'email', headerName: 'Email', width: 230 },
    { field: 'zone', headerName: 'Zone de Suivi', width: 150 },
  ];

  const actionColumn = [
    {
      field: 'action',
      headerName: 'Action',
      width: 200,
      renderCell: (params) => {
        return (
          <div className="cellAction">
            <div className="viewButton" onClick={() => handleView(params.row)}>
              Consulter
            </div>
            <div className="deleteButton" onClick={() => handleDelete(params.row)}>
              Supprimer
            </div>
          </div>
        );
      },
    },
  ];

  return (
    <div className="datatable">
      <div className="datatableTitle" style={{ color: '#00A2DD' }}>
        Gestion des Responsables des Suivis
        <Link to="/ajouter_responsable_suivi" className="link">
          <PersonAddIcon></PersonAddIcon>Ajouter un nouveau responsable
        </Link>
      </div>
      <DataGrid
        className="datagrid"
        rows={data}
        columns={userColumns.concat(actionColumn)}
        pageSize={9}
        rowsPerPageOptions={[9]}
        checkboxSelection
        getRowId={(row) => row.id} // Utilisez la clé unique de vos données
      />
    </div>
  );
};

export default Datatable_suivi;