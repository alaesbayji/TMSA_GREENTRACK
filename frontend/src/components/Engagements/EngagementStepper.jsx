import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Stepper, Step, StepLabel, Button, TextField, Paper, Typography, MenuItem } from '@mui/material';
import './EngagementStepper.scss'; // Fichier SCSS pour le style

const EngagementStepper = () => {
  const [activeStep, setActiveStep] = useState(0); // Étape active du stepper
  const [engagementAspect, setEngagementAspect] = useState({
    id_entreprise: '', // ID entreprise sélectionné
    id_aspect: '', // ID aspect sélectionné
    id_sous_aspect: null,
    lieu_prelevement: '',
    methode_equipement: '',
    frequence: '', // Fréquence sélectionnée
    responsabilite: '',
    date_creation: new Date().toISOString().split('T')[0], // Date du jour
  });
  const [engagementIndicateurs, setEngagementIndicateurs] = useState([]);
  const [currentIndicateur, setCurrentIndicateur] = useState({
    id_indicateur: '',
    id_engagement_aspect: null, // Rempli après la création de l'engagement aspect
  });

  // États pour les listes
  const [aspects, setAspects] = useState([]); // Liste des aspects
  const [entreprises, setEntreprises] = useState([]); // Liste des entreprises
  const [frequences, setFrequences] = useState([
    { label: 'Mensuel', value: 1 },
    { label: 'Trimestriel', value: 2 },
    { label: 'Semestriel', value: 3 },
    { label: 'Bisannuel', value: 4 },
    { label: 'Triennal', value: 5 },
  ]);
  const [indicateurs, setIndicateurs] = useState([]); // Liste des indicateurs
  const [sousAspectsEau, setSousAspectsEau] = useState([]); // Liste des sous-aspects eau

  // Charger les aspects, les entreprises et les indicateurs au montage du composant
  useEffect(() => {
    const fetchAspects = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/aspect/');
        setAspects(response.data);
      } catch (error) {
        console.error('Erreur lors du chargement des aspects :', error);
      }
    };

    const fetchEntreprises = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/entreprise/');
        setEntreprises(response.data);
      } catch (error) {
        console.error('Erreur lors du chargement des entreprises :', error);
      }
    };

    fetchAspects();
    fetchEntreprises();
  }, []);

  // Charger les sous-aspects eau si l'aspect sélectionné est de type "eau"
  useEffect(() => {
    const fetchSousAspectsEau = async () => {
      if (engagementAspect.id_aspect) {
        const selectedAspect = aspects.find((aspect) => aspect.id_aspect === engagementAspect.id_aspect);
        if (selectedAspect && selectedAspect.est_eau) {
          try {
            const response = await axios.get('http://localhost:8000/api/sous-aspects-eau-pollution/');
            setSousAspectsEau(response.data);
          } catch (error) {
            console.error('Erreur lors du chargement des sous-aspects eau :', error);
          }
        } else {
          setSousAspectsEau([]); // Réinitialiser si l'aspect n'est pas de type "eau"
        }
      }
    };

    fetchSousAspectsEau();
  }, [engagementAspect.id_aspect, aspects]);

  // Charger les indicateurs en fonction du type d'aspect et de sous-aspect
  useEffect(() => {
    const fetchIndicateurs = async () => {
      try {
        let url = 'http://localhost:8000/api/indicateur/';
        const selectedAspect = aspects.find((aspect) => aspect.id_aspect === engagementAspect.id_aspect);
        const selectedSousAspectEau = sousAspectsEau.find(
          (sousAspect) => sousAspect.id_sous_aspect === engagementAspect.id_sous_aspect
        );
  
        if (selectedAspect && selectedAspect.est_eau) {
          if (selectedSousAspectEau && selectedSousAspectEau.est_pollution) {
            url = 'http://localhost:8000/api/indicateurs-eau-pollution/';
          } else {
            url = 'http://localhost:8000/api/indicateurs-sous-aspect/';
          }
        }
  
        const response = await axios.get(url);
  
        // Normaliser les indicateurs en fonction de l'API utilisée
        const normalizedIndicateurs = response.data.map((indicateur) => {
          if (url === 'http://localhost:8000/api/indicateurs-eau-pollution/') {
            return {
              id_indicateur: indicateur.id_indicateur_eaupollution, // Utiliser id_indicateur_sous_aspect
              nom: indicateur.nom,
            };
          } 
          else if (url === 'http://localhost:8000/api/indicateurs-sous-aspect/'){
            return { 
            id_indicateur: indicateur.id_indicateur_sous_aspect, // Utiliser id_indicateur_sous_aspect
              nom: indicateur.nom,
            }
          }
          else {
            return {
              id_indicateur: indicateur.id_indicateur, // Utiliser id_indicateur
              nom: indicateur.nom,
            };
          }
        });
  
        setIndicateurs(normalizedIndicateurs);
      } catch (error) {
        console.error('Erreur lors du chargement des indicateurs :', error);
      }
    };
  
    fetchIndicateurs();
  }, [engagementAspect.id_aspect, engagementAspect.id_sous_aspect, aspects, sousAspectsEau]);

  // Gérer le changement des champs de l'engagement aspect
  const handleEngagementAspectChange = (e) => {
    const { name, value } = e.target;
    setEngagementAspect((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Gérer le changement des champs de l'engagement indicateur
  const handleIndicateurChange = (e) => {
    const { name, value } = e.target;
    setCurrentIndicateur((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Passer à l'étape suivante
  const handleNext = () => {
    setActiveStep((prev) => prev + 1);
  };

  // Revenir à l'étape précédente
  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  // Soumettre l'engagement aspect
  const submitEngagementAspect = async () => {
    try {
      let response;
      const selectedAspect = aspects.find((aspect) => aspect.id_aspect === engagementAspect.id_aspect);
      const selectedSousAspectEau = sousAspectsEau.find(
        (sousAspect) => sousAspect.id_sous_aspect === engagementAspect.id_sous_aspect
      );

      if (selectedAspect && selectedAspect.est_eau) 
        {
        if (selectedSousAspectEau && selectedSousAspectEau.est_pollution) {
          // Cas : Sous-aspect eau avec pollution
          console.log(engagementAspect)
          response = await axios.post('http://localhost:8000/api/engagements/sous-aspect-pollution/', engagementAspect);
        } else {
            alert(selectedSousAspectEau)
          // Cas : Sous-aspect eau sans pollution
          console.log(engagementAspect)

          response = await axios.post('http://localhost:8000/api/engagements-sous-aspect/', engagementAspect);
        }
      } else {
        // Cas : Aspect non-eau
        console.log(engagementAspect)

        response = await axios.post('http://localhost:8000/api/engagement-aspect/', engagementAspect);
      }

      alert('Engagement aspect créé avec succès !');
      setCurrentIndicateur((prev) => ({
        ...prev,
        id_engagement_aspect: response.data.id_engagement_aspect, // Lier l'engagement aspect créé
      }));
      handleNext(); // Passer à l'étape suivante
    } catch (error) {
      console.error('Erreur lors de la création de l\'engagement aspect :', error);
      alert('Erreur lors de la création de l\'engagement aspect.');
    }
  };

  // Ajouter un engagement indicateur
  const addEngagementIndicateur = async () => {
    if (!currentIndicateur.id_indicateur) {
      alert('Veuillez sélectionner un indicateur.');
      return;
    }

    try {
      let url = 'http://localhost:8000/api/engagements-indicateur/';
      const selectedAspect = aspects.find((aspect) => aspect.id_aspect === engagementAspect.id_aspect);
      const selectedSousAspectEau = sousAspectsEau.find(
        (sousAspect) => sousAspect.id_sous_aspect === engagementAspect.id_sous_aspect
      );

      if (selectedAspect && selectedAspect.est_eau) {
        if (selectedSousAspectEau && selectedSousAspectEau.est_pollution) {
          url = 'http://localhost:8000/api/indicateurs/sous-aspect-pollution/';
        } else {
          url = 'http://localhost:8000/api/engagementsindicateur-sous-aspect/';
        }
      }

      await axios.post(url, currentIndicateur);
      alert('Engagement indicateur ajouté avec succès !');
      setEngagementIndicateurs((prev) => [...prev, currentIndicateur]);
      setCurrentIndicateur({
        id_indicateur: '',
        id_engagement_aspect: currentIndicateur.id_engagement_aspect, // Conserver l'ID de l'engagement aspect
      });
    } catch (error) {
      console.error('Erreur lors de l\'ajout de l\'engagement indicateur :', error);
      alert('Erreur lors de l\'ajout de l\'engagement indicateur.');
    }
  };

  // Soumettre tous les engagements
  const submitAll = () => {
    alert('Tous les engagements ont été soumis avec succès !');
    // Réinitialiser le formulaire
    setActiveStep(0);
    setEngagementAspect({
      id_entreprise: '',
      id_aspect: '',
      id_sous_aspect: null,
      lieu_prelevement: '',
      methode_equipement: '',
      frequence: '',
      responsabilite: '',
      date_creation: new Date().toISOString().split('T')[0],
    });
    setEngagementIndicateurs([]);
    setCurrentIndicateur({
      id_indicateur: '',
      id_engagement_aspect: null,
    });
  };

  return (
    <Paper elevation={3} className="stepperContainer">
      <Typography variant="h4" gutterBottom>
        Créer un Engagement
      </Typography>
      <Stepper activeStep={activeStep} alternativeLabel>
        <Step>
          <StepLabel>Engagement Aspect</StepLabel>
        </Step>
        <Step>
          <StepLabel>Engagements Indicateurs</StepLabel>
        </Step>
      </Stepper>

      {activeStep === 0 && (
        <div className="stepContent">
          <Typography variant="h6" gutterBottom>
            Étape 1 : Engagement Aspect
          </Typography>

          {/* Liste déroulante pour les entreprises */}
          <TextField
            select
            label="Entreprise"
            name="id_entreprise"
            value={engagementAspect.id_entreprise}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          >
            {entreprises.map((entreprise) => (
              <MenuItem key={entreprise.id_entreprise} value={entreprise.id_entreprise}>
                {entreprise.nom}
              </MenuItem>
            ))}
          </TextField>

          {/* Liste déroulante pour les aspects */}
          <TextField
            select
            label="Aspect"
            name="id_aspect"
            value={engagementAspect.id_aspect}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          >
            {aspects.map((aspect) => (
              <MenuItem key={aspect.id_aspect} value={aspect.id_aspect}>
                {aspect.typeMilieu}
              </MenuItem>
            ))}
          </TextField>

          {/* Liste déroulante pour les sous-aspects eau (si l'aspect est de type "eau") */}
          {engagementAspect.id_aspect && aspects.find((aspect) => aspect.id_aspect === engagementAspect.id_aspect)?.est_eau && (
            <TextField
              select
              label="Sous-Aspect Eau"
              name="id_sous_aspect"
              value={engagementAspect.id_sous_aspect || ''}
              onChange={handleEngagementAspectChange}
              fullWidth
              margin="normal"
              required
            >
              {sousAspectsEau.map((sousAspect) => (
                <MenuItem key={sousAspect.id_sous_aspect} value={sousAspect.id_sous_aspect}>
                  {sousAspect.nom}
                </MenuItem>
              ))}
            </TextField>
          )}

          {/* Champ pour la date de création */}
          <TextField
            label="Date de Création"
            type="date"
            name="date_creation"
            value={engagementAspect.date_creation}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
            InputLabelProps={{
              shrink: true,
            }}
          />

          {/* Liste déroulante pour les fréquences */}
          <TextField
            select
            label="Fréquence"
            name="frequence"
            value={engagementAspect.frequence}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          >
            {frequences.map((freq) => (
              <MenuItem key={freq.value} value={freq.value}>
                {freq.label}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            label="Lieu de Prélèvement"
            name="lieu_prelevement"
            value={engagementAspect.lieu_prelevement}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Méthode/Équipement"
            name="methode_equipement"
            value={engagementAspect.methode_equipement}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Responsabilité"
            name="responsabilite"
            value={engagementAspect.responsabilite}
            onChange={handleEngagementAspectChange}
            fullWidth
            margin="normal"
            required
          />
          <Button variant="contained" color="primary" onClick={submitEngagementAspect}>
            Suivant
          </Button>
        </div>
      )}

      {activeStep === 1 && (
        <div className="stepContent">
          <Typography variant="h6" gutterBottom>
            Étape 2 : Engagements Indicateurs
          </Typography>

          {/* Liste déroulante pour les indicateurs */}
          <TextField
            select
            label="Indicateur"
            name="id_indicateur"
            value={currentIndicateur.id_indicateur}
            onChange={handleIndicateurChange}
            fullWidth
            margin="normal"
            required
          >
            {indicateurs.map((indicateur) => (
              <MenuItem key={indicateur.id_indicateur} value={indicateur.id_indicateur}>
                {indicateur.nom}
              </MenuItem>
            ))}
          </TextField>

          <Button variant="contained" color="primary" onClick={addEngagementIndicateur}>
            Ajouter un Indicateur
          </Button>
          <Button variant="contained" color="secondary" onClick={submitAll}>
            Terminer
          </Button>
          <Button variant="outlined" onClick={handleBack}>
            Retour
          </Button>
        </div>
      )}
    </Paper>
  );
};

export default EngagementStepper;