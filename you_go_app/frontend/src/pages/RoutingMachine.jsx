// RoutingMachine.jsx
import { useMap } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';

const RoutingMachine = ({ start, end, onRouteInfo }) => {
    const map = useMap();

    useEffect(() => {
        if (!map || !start || !end) return;

        const control = L.Routing.control({
            waypoints: [L.latLng(start[0], start[1]), L.latLng(end[0], end[1])],
            show: false,
            addWaypoints: false,
            routeWhileDragging: false,
            lineOptions: { styles: [{ color: '#3b82f6', weight: 5 }] },
            createMarker: () => null,
            router: L.Routing.mapbox('YOUR_MAPBOX_ACCESS_TOKEN_HERE'),
        }).addTo(map);

        control.on('routesfound', (e) => {
            const summary = e.routes[0].summary;
            const distanceKm = (summary.totalDistance / 1000).toFixed(2);
            const timeMin = Math.round(summary.totalTime / 60);
            onRouteInfo({ distanceKm, timeMin });
        });

        return () => map.removeControl(control);
    }, [map, start, end, onRouteInfo]);

    return null;
};

export default RoutingMachine;
