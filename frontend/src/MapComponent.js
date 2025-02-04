import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function MapComponent() {
  return (
    <MapContainer center={[35.6895, -5.9078]} zoom={13} style={{ height: "500px", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[35.6895, -5.9078]}>
        <Popup>Test popup</Popup>
      </Marker>
    </MapContainer>
  );
}

export default MapComponent;
