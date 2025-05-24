import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

import { useFetch } from "../../hooks";
import { HeatmapResponse } from "../../models/models";

const ACCESS_TOKEN = 'pk.eyJ1IjoiYXZyMjE2IiwiYSI6ImNtYjA4c2pwdDByZWkya29wZXRiczI2NWMifQ.WXExsenqK2KCdhX60ERqJQ'

const LOCAL_API_HACKER_URL = 'http://localhost:5002/api/v1/ransomware';

export const Heatmap = () => {
    
    const {data, loading, error } = useFetch<HeatmapResponse>(`${LOCAL_API_HACKER_URL}/heatmap`)

    const mapContainerRef = useRef<HTMLDivElement>(null);

    mapboxgl.accessToken = ACCESS_TOKEN;

    useEffect(() => {
        if(!mapboxgl.accessToken) {
            console.error('missing token');
            return;
        }
        if (!mapContainerRef.current) return;

        if(!data) return;

        const map = new mapboxgl.Map({
        container: mapContainerRef.current,
        style: 'mapbox://styles/mapbox/dark-v10',
        center: [0, 20],
        zoom: 1.5,
        });

        map.on('load', () => {
            const geojson: GeoJSON.FeatureCollection = {
                type: 'FeatureCollection',
                features: data.heatmap_info.map(p => ({
                    type: 'Feature',
                    geometry: {
                    type: 'Point',
                    coordinates: [p.lng, p.lat],
                },
                 properties: {
                    weight: p.victims,
                    name: p.name,
                    group: p.top_group
                    },
                }))
            };
        map.addSource('heatmap-source', {
                type: 'geojson',
                data: geojson,
        });

        map.addLayer({
        id: 'heatmap-layer',
        type: 'heatmap',
        source: 'heatmap-source',
        paint: {
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'weight'], 0, 0, 100, 1],
          'heatmap-intensity': 1,
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(0,0,255,0)',
            0.4, 'royalblue',
            0.6, 'cyan',
            0.8, 'lime',
            1, 'red'
          ],
          'heatmap-radius': 20,
        },
      });

      // 4) Capa de puntos invisibles para capturar hover
      map.addLayer({
        id: 'point-layer',
        type: 'circle',
        source: 'heatmap-source',
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'weight'],
            0,    10,    // 0 victims → 10px
            100,  20,   // 100 victims → 20px
            1000, 40    // 1000 victims → 40px
            ],
          'circle-color': 'rgba(255, 0, 0, 0.5)',
          'circle-opacity': 0.7,
          'circle-blur': 0.6
        }
      });

      // 5) Eventos para tooltip
      let popup: mapboxgl.Popup;
      map.on('mouseenter', 'point-layer', (e) => {
        map.getCanvas().style.cursor = 'pointer';
        const feature = e.features![0];
        const coords = (feature.geometry as any).coordinates as [number, number];
        const props = feature.properties as any;
        const victims = props.weight as number;
        const name = props.name as string;
        const group = props.group as string;
        popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false
        })
        .setLngLat(coords)
        .setHTML(`<div style="text-align:center">          
                <strong>${name}</strong><br/>
                Attacks: ${victims} <br/>
                Group: ${group} <br/>
            </div>`)
        .addTo(map);
      });
      map.on('mouseleave', 'point-layer', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
      });
    });

    return () => {
      // Destroy subscription to events
      map.remove()
    }
    
    }, [data]);

    if (loading) {
        return <h1>Loading...</h1>
    }

    if(error) {
        return <h1>Error: {error.message}</h1>
    }

    return (
        <section aria-label="Heatmap attacks" className="bg-[#1a1a1a] text-gray-500 h-screen flex flex-col">
        <header className="p-4">
          <h1 className="text-2xl font-bold text-center">Heatmap of ransomware attacks</h1>
        </header>
          <div 
            ref={mapContainerRef}
            className="w-[90%] h-[80vh] rounded-lg shadow-lg p-3 mx-auto"
          />
      </section>
    )
}