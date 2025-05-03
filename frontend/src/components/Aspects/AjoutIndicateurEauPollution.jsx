import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import './DatatableAspect.scss';

const AjoutIndicateurPollutionForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { sousAspectId: initialSousAspectId } = location.state || {}; // Récupérer l'id_sous_aspect depuis le state

  const [indicateurs, setIndicateurs] = useState([]);
  const [currentIndicateur, setCurrentIndicateur] = useState(null);
  const [nom, setNom] = useState('');
  const [seuilMax, setSeuilMax] = useState('');
  const [unite, setUnite] = useState('');
  const [codeMICNT, setCodeMICNT] = useState('');
  const [idActivite, setIdActivite] = useState('');
  const [loading, setLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const [message, setMessage] = useState('');

  // États pour les données chargées
  const [secteurs, setSecteurs] = useState([]);
  const [activites, setActivites] = useState([]);
  const [selectedSecteur, setSelectedSecteur] = useState('');
  const [sousAspects, setSousAspects] = useState([]); // État pour stocker la liste des sous-aspects
  const [sousAspectId, setSousAspectId] = useState(initialSousAspectId || ''); // État pour le sous-aspect sélectionné

  // Charger les secteurs au montage du composant
  useEffect(() => {
    const loadData = async () => {
      try {
        const secteursResponse = await axios.get('http://localhost:8000/api/secteurs/');
        setSecteurs(secteursResponse.data);
      } catch (error) {
        alert('Erreur lors du chargement des secteurs');
      }
    };

    loadData();
  }, []);

  // Charger la liste des sous-aspects au montage du composant
  useEffect(() => {
    const fetchSousAspects = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/sous-aspects-eau-pollution/');
        const filteredAspects = response.data.filter(aspect => aspect.est_pollution === true);
        setSousAspects(filteredAspects);
      } catch (error) {
        console.error('Error fetching sous-aspects:', error);
        alert('Erreur lors du chargement des sous-aspects.');
      }
    };

    fetchSousAspects();
  }, []);

  // Charger les indicateurs pour le sous-aspect sélectionné
  useEffect(() => {
    const fetchData = async () => {
      if (!sousAspectId) return; // Ne pas charger si aucun sous-aspect n'est sélectionné

      try {
        const response = await axios.get(`http://localhost:8000/api/indicateurs-eau-pollution/?id_sous_aspect=${sousAspectId}`);
        const indicateursData = response.data;

        // Enrichir les données avec les noms des activités et des secteurs
        const enrichedIndicateurs = await Promise.all(
          indicateursData.map(async (indicateur) => {
            const activiteResponse = await axios.get(`http://localhost:8000/api/activites-industrielles/${indicateur.id_activite}/`);
            const secteurResponse = await axios.get(`http://localhost:8000/api/secteurs/${activiteResponse.data.id_secteur}/`);

            return {
              ...indicateur,
              nom_activite: activiteResponse.data.nom,
              nom_secteur: secteurResponse.data.nom,
            };
          })
        );

        setIndicateurs(enrichedIndicateurs);
      } catch (error) {
        console.error('Error fetching indicateurs:', error);
        alert('Erreur lors du chargement des indicateurs.');
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, [sousAspectId]);

  // Gérer le changement de secteur
  const handleSecteurChange = async (e) => {
    const secteurId = e.target.value;
    setSelectedSecteur(secteurId);

    if (secteurId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/activites-industriellesbyid/?id_secteur=${secteurId}`);
        setActivites(response.data);
      } catch (error) {
        alert('Erreur lors du chargement des activités');
      }
    } else {
      setActivites([]);
    }
  };

  // Gérer le changement de sous-aspect
  const handleSousAspectChange = (e) => {
    const selectedSousAspectId = e.target.value;
    setSousAspectId(selectedSousAspectId); // Mettre à jour le sous-aspect sélectionné
  };

  // Ajouter ou mettre à jour un indicateur de pollution
  const addOrUpdateIndicateur = async (e) => {
    e.preventDefault();
    setLoading(true);

    const indicateurData = {
      nom,
      seuil_max: parseFloat(seuilMax),
      unite,
      code_MICNT: parseInt(codeMICNT, 10),
      id_sous_aspect: sousAspectId,
      id_activite: parseInt(idActivite, 10),
    };

    try {
      let response;
      if (currentIndicateur) {
        response = await axios.put(
          `http://localhost:8000/api/indicateurs-eau-pollution/${currentIndicateur.id_indicateur_eaupollution}/`,
          indicateurData
        );
      } else {
        response = await axios.post('http://localhost:8000/api/indicateurs-eau-pollution/', indicateurData);
      }

      const newIndicateur = {
        id_indicateur_eaupollution: response.data.id_indicateur_eaupollution,
        nom: response.data.nom,
        seuil_max: response.data.seuil_max,
        unite: response.data.unite,
        code_MICNT: response.data.code_MICNT,
        id_sous_aspect: response.data.id_sous_aspect,
        id_activite: response.data.id_activite,
      };

      if (currentIndicateur) {
        setIndicateurs((prev) =>
          prev.map((i) => (i.id_indicateur_eaupollution === newIndicateur.id_indicateur_eaupollution ? newIndicateur : i))
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

  // Supprimer un indicateur de pollution
  const deleteIndicateur = async (id_indicateur_eaupollution) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cet indicateur ?')) {
      try {
        await axios.delete(`http://localhost:8000/api/indicateurs-eau-pollution/${id_indicateur_eaupollution}/`);
        setIndicateurs((prev) => prev.filter((i) => i.id_indicateur_eaupollution !== id_indicateur_eaupollution));
        alert('Indicateur supprimé avec succès!');
      } catch (error) {
        console.error('Error:', error);
        alert(`Erreur lors de la suppression: ${error.response?.data?.error || error.message}`);
      }
    }
  };

  // Modifier un indicateur de pollution
  const handleEditIndicateur = (indicateur) => {
    setCurrentIndicateur(indicateur);
    setNom(indicateur.nom);
    setSeuilMax(indicateur.seuil_max);
    setUnite(indicateur.unite);
    setCodeMICNT(indicateur.code_MICNT);
    setIdActivite(indicateur.id_activite);
  };

  // Réinitialiser le formulaire
  const resetIndicateurForm = () => {
    setCurrentIndicateur(null);
    setNom('');
    setSeuilMax('');
    setUnite('');
    setCodeMICNT('');
    setIdActivite('');
  };

  // Colonnes pour la DataGrid
  const columnsIndicateurs = [
    { field: 'id', headerName: 'ID', flex: 0.1 },
    { field: 'nom', headerName: 'Nom', flex: 0.5 },
    { field: 'seuil_max', headerName: 'Seuil Max', flex: 0.5 },
    { field: 'unite', headerName: 'Unité', flex: 0.5 },
    { field: 'code_MICNT', headerName: 'Code MICNT', flex: 0.5 },
    { field: 'nom_activite', headerName: 'Activité', flex: 1 },
    { field: 'nom_secteur', headerName: 'Secteur', flex: 1 },
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
          <button className="deleteButton" onClick={() => deleteIndicateur(params.row.id_indicateur_eaupollution)}>
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
      <h2>Gestion des Indicateurs de Pollution</h2>
      <div className="formInput">
        <label>Sélectionnez un sous-aspect :</label>
        <select value={sousAspectId} onChange={handleSousAspectChange} required>
          <option value="">Sélectionnez un sous-aspect</option>
          {sousAspects.map((sousAspect) => (
            <option key={sousAspect.id_sous_aspect} value={sousAspect.id_sous_aspect}>
              {sousAspect.nom}
            </option>
          ))}
        </select>
      </div>

      {sousAspectId && (
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
            <div className="formInput">
              <label>Code MICNT :</label>
              <input
                type="number"
                value={codeMICNT}
                onChange={(e) => setCodeMICNT(e.target.value)}
                required
              />
            </div>
            <div className="formInput">
              <label>Secteur :</label>
              <select
                value={selectedSecteur}
                onChange={handleSecteurChange}
                required
              >
                <option value="">Sélectionnez un secteur</option>
                {secteurs.map((secteur) => (
                  <option key={secteur.id_secteur} value={secteur.id_secteur}>
                    {secteur.nom}
                  </option>
                ))}
              </select>
            </div>
            <div className="formInput">
              <label>Activité :</label>
              <select
                value={idActivite}
                onChange={(e) => setIdActivite(e.target.value)}
                required
                disabled={!selectedSecteur}
              >
                <option value="">Sélectionnez une activité</option>
                {activites.map((activite) => (
                  <option key={activite.id_activite} value={activite.id_activite}>
                    {activite.nom}
                  </option>
                ))}
              </select>
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
              rows={indicateurs.map((indicateur) => ({ ...indicateur, id: indicateur.id_indicateur_eaupollution }))}
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

export default AjoutIndicateurPollutionForm;