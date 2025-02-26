import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { MapContainer, TileLayer, Polygon, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './Ajouter_entreprise1.scss';
import Sidebar from '../../components/Sidebar/Sidebar';
import Navbar from '../../components/Navbar/Navbar';
import wellknown from 'wellknown';
import proj4 from 'proj4';

const EPSG26191 = '+proj=lcc +lat_1=33.3 +lat_0=33.3 +lon_0=-5.4 +k_0=0.999625769 +x_0=500000 +y_0=300000 +ellps=clrk80ign +towgs84=31,146,47,0,0,0,0 +units=m +no_defs';
const EPSG4326 = 'EPSG:4326';

function Ajouter_entreprise1() {
  const [shapefile, setShapefile] = useState(null);
  const [parcelles, setParcelles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedParcelleId, setSelectedParcelleId] = useState(null);
  const [occupiedParcelleIds, setOccupiedParcelleIds] = useState([]);
  const [popupContent, setPopupContent] = useState(null);
  const [popupPosition, setPopupPosition] = useState(null);
  const navigate = useNavigate();

  const handleShapefileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.zip')) {
      setShapefile(file);
    } else {
      alert('Veuillez sélectionner un fichier ZIP contenant un Shapefile valide.');
    }
  };

  const handleShapefileUpload = async () => {
    if (!shapefile) {
      alert('Veuillez sélectionner un fichier ZIP.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('shapefile', shapefile);

    try {
      const response = await axios.post('http://localhost:8000/api/import-shapefile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
      loadParcelles();
    } catch (error) {
      alert(`Erreur lors de l'importation du shapefile: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const loadOccupiedParcelles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/entreprise/');
      const ids = response.data.map(entreprise => entreprise.id_parcelle);
      setOccupiedParcelleIds(ids);
    } catch (error) {
      alert('Erreur lors du chargement des parcelles occupées');
    }
  };

  const loadParcelles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/parcelles/');
      setParcelles(response.data);
      await loadOccupiedParcelles();
    } catch (error) {
      alert('Erreur lors du chargement des parcelles');
    }
  };

  useEffect(() => {
    loadParcelles();
  }, []);

  return (
    <div className="new">
      <Sidebar />
      <div className="newContainer">
        <Navbar />
        <div className="top">
          <h1>Ajouter Une Entreprise</h1>
        </div>
        <div className="bottom">
          {/* <div>
            <input type="file" accept=".zip" onChange={handleShapefileChange} />
            <button onClick={handleShapefileUpload} disabled={loading}>
              {loading ? 'Importation en cours...' : 'Importer Shapefile'}
            </button>
          </div> */}
          <MapContainer center={[35.7200, -5.9085]} zoom={14} style={{ height: "500px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {parcelles.map(parcelle => {
              if (parcelle.geom) {
                const geoJson = wellknown(parcelle.geom);
                const originalCoords = geoJson.coordinates[0].map(coord => [coord[0], coord[1]]);
                const transformedCoords = originalCoords.map(coord => {
                  const [x, y] = proj4(EPSG26191, EPSG4326, [coord[0], coord[1]]);
                  return [y, x];
                });

                const isOccupied = occupiedParcelleIds.includes(parcelle.id_parcelle);

                return (
                  <Polygon
                    key={parcelle.id_parcelle}
                    positions={transformedCoords}
                    pathOptions={{ color: isOccupied ? 'red' : 'green' }}
                    eventHandlers={{
                      click: (e) => {
                        if (!isOccupied) {
                          setSelectedParcelleId(parcelle.id_parcelle);
                          setPopupContent(`ID de la parcelle: ${parcelle.id_parcelle}`);
                          setPopupPosition(e.latlng);
                        } else {
                          setPopupContent('Cette parcelle est déjà occupée par une entreprise.');
                          setPopupPosition(e.latlng);
                        }
                      },
                    }}
                  />
                );
              } else {
                console.warn(`Parcelle avec ID ${parcelle.id_parcelle} n'a pas de géométrie valide.`);
                return null;
              }
            })}
            {popupContent && popupPosition && (
              <Popup position={popupPosition} onClose={() => setPopupContent(null)}>
                {popupContent}
              </Popup>
            )}
          </MapContainer>

          {selectedParcelleId && (
            <button className="button" onClick={() => navigate('/ajouter_entreprise2', { state: { id_parcelle: selectedParcelleId } })}>
              Next 
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Ajouter_entreprise1;