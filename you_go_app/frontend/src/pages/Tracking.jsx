// Tracking.jsx
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';
import L from 'leaflet';
import { useEffect, useState } from 'react';
import Navbar from "../components/Navbar";
import UserIcon from '../assets/icons/marker1.png';
import ContactIcon from '../assets/icons/marker2.png';
import RecenterMap from './RecenterMap';

delete L.Icon.Default.prototype._getIconUrl;

const userIcon = new L.Icon({
  iconUrl: UserIcon,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});
const contactIcon = new L.Icon({
  iconUrl: ContactIcon,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});

// Haversine formula to compute distance in km
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // km
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
    Math.cos(lat2 * (Math.PI / 180)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function Tracking() {
  const [driverPosition, setDriverPosition] = useState([6.5, 2.6]); // Default Benin coords
  const [passengerPosition] = useState([6.495, 2.605]); // Mocked passenger coords

  const distance = getDistanceFromLatLonInKm(
    driverPosition[0],
    driverPosition[1],
    passengerPosition[0],
    passengerPosition[1]
  ).toFixed(2);

  const averageSpeedKmh = 40;
  const estimatedTime = (distance / averageSpeedKmh * 60).toFixed(1); // in minutes

  useEffect(() => {
    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        setDriverPosition([latitude, longitude]);
      },
      (err) => console.error(err),
      { enableHighAccuracy: true, maximumAge: 10000 }
    );
    return () => navigator.geolocation.clearWatch(watchId);
  }, []);

  return (
    <div className='relative w-full h-screen'>
      <MapContainer center={driverPosition} zoom={15} scrollWheelZoom={true} className="absolute z-1 w-full h-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        
        {/* Driver marker */}
        <Marker position={driverPosition} icon={userIcon}>
          <Popup>Votre position (Conducteur)</Popup>
        </Marker>

        {/* Passenger marker */}
        <Marker position={passengerPosition} icon={contactIcon}>
          <Popup>Position du passager</Popup>
        </Marker>

        {/* Draw line between driver and passenger */}
        <Polyline positions={[driverPosition, passengerPosition]} color="blue" />
        <RecenterMap position={driverPosition} />
      </MapContainer>

      <div className='absolute bottom-[18vh] left-1/2 transform -translate-x-1/2 w-[90%] max-w-xl px-4 py-3 bg-white rounded-2xl shadow-md z-10 text-gray-800'>
        <h3 className="text-lg font-semibold">Informations de trajet</h3>
        <p>Distance estimée: <span className="font-bold">{distance} km</span></p>
        <p>Temps estimé: <span className="font-bold">{estimatedTime} minutes</span></p>
      </div>

      <Navbar />
    </div>
  );
}

export default Tracking;
