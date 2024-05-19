import React, { useEffect, useRef, useState, useMemo } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';

const MapComponent = ({ start, end, handleRouteLoads, buttonText }) => {
    const mapRef = useRef(null);
    const [routeLoaded, setRouteLoaded] = useState(false);
    const [routeKey, setRouteKey] = useState('');

    // La clave de la ruta depende de las coordenadas de inicio y fin, así como del estado buttonText
    useEffect(() => {
        setRouteKey(`${start.lat},${start.lng}-${end.lat},${end.lng}-${buttonText}`);
    }, [start, end, buttonText]);

    useEffect(() => {
        const map = mapRef.current;

        if (!map) return;

        const control = L.Routing.control({
            waypoints: [L.latLng(start.lat, start.lng), L.latLng(end.lat, end.lng)],
            routeWhileDragging: true,
            lineOptions: {
                styles: [{ color: '#000', opacity: 0.8, weight: 5 }],
                addWaypoints: false,
                draggableWaypoints: false
            },
            router: L.Routing.osrmv1({
                language: 'es',
            }),
        }).addTo(map);

        // Establecer el estado de ruta cargada cuando se carga la ruta
        control.on('routesfound', () => {
            setRouteLoaded(true);
        });

        // Limpiar el controlador de ruta al desmontar el componente
        return () => {
            map.removeControl(control);
        };
    }, [routeKey]);

    useEffect(() => {
        // Cambiar el color del texto de las instrucciones
        const instructionsElements = document.querySelectorAll('.leaflet-routing-container.leaflet-routing-collapsed td');
        instructionsElements.forEach(element => {
            element.style.color = '#000'; // Cambia el color del texto a negro
        });
    }, []);

    return (
        <>
            <MapContainer center={[start.lat, start.lng]} zoom={13} style={{ height: '500px', width: '100%' }} ref={mapRef}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />
            </MapContainer>
        </>
    );
};

export default MapComponent;
