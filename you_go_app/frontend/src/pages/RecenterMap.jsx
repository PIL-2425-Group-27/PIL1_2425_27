import { useMap } from 'react-leaflet';
import { useEffect } from 'react';

const RecenterMap = ({ position }) => {
  const map = useMap();

  useEffect(() => {
    map.setView(position, map.getZoom());
  }, [position, map]);

  return null;
};

export default RecenterMap;
