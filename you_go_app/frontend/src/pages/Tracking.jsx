// App.jsx or MapTracker.jsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect, useState } from 'react';
import Navbar from "../components/Navbar";
import MarkerIcon from '../assets/icons/marker1.png'; // adjust path as needed



// Fix Leaflet's default icon issue in React
delete L.Icon.Default.prototype._getIconUrl;

const icon = new L.Icon({
  iconUrl: MarkerIcon,
  iconSize: [38, 38], // width, height
  iconAnchor: [19, 38], // point of the icon which will correspond to marker's location
  popupAnchor: [0, -38], // point from which the popup should open relative to the iconAnchor
});

function Tracking() {
    const [position, setPosition] = useState([6.5, 2.6]); // example coords (Benin)

    useEffect(() => {
        const watchId = navigator.geolocation.watchPosition(
            (pos) => {
                const { latitude, longitude } = pos.coords;
                setPosition([latitude, longitude]);
            },
            (err) => console.error(err),
            { enableHighAccuracy: true, maximumAge: 10000 }
        );
        return () => navigator.geolocation.clearWatch(watchId);
    }, []);

    return (
        <>
            <div className='relative w-full h-screen'>
                <div className="w-full h-screen">
                    <MapContainer center={position} zoom={15} scrollWheelZoom={true} className="absoolute z-1 w-full h-full">
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        <Marker position={position} icon={icon}>
                            <Popup>Votre position actuelle</Popup>
                        </Marker>
                    </MapContainer>
                </div>
                <div className=' absolute z-20 w-[90%] h-16 bg-red-300 '>

                </div>
                <Navbar />
            </div>
        </>
    );
}


export default Tracking;