// App.jsx or MapTracker.jsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect, useState } from 'react';
import Navbar from "../components/Navbar";


// Fix Leaflet's default icon issue in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
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
                        <Marker position={position}>
                            <Popup>Your current location</Popup>
                        </Marker>
                    </MapContainer>
                </div>
                <Navbar />
            </div>
        </>
    );
}


export default Tracking;