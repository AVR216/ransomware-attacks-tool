import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

import { HeatmapResponse } from "../../models/models";

import { useFetch, useModalContext } from "../../hooks";
import { Loading } from "../Loading/Loading";
import { ErrorDisplay } from "../Error/ErrorDisplay";
import { MAPBOX_TOKEN, API_BASE_URL } from '../../config'

export const Heatmap = () => {
  const { data, loading, error } = useFetch<HeatmapResponse>(`${API_BASE_URL}/heatmap`);

  const mapContainerRef = useRef<HTMLDivElement>(null);

  const { openModal } = useModalContext();
  
  mapboxgl.accessToken = MAPBOX_TOKEN;

  useEffect(() => {
    if (!mapboxgl.accessToken) {
      console.error('missing token');
      return;
    }
    if (!mapContainerRef.current || !data) return;

    // Map instance
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/dark-v10',
      center: [0, 20],
      zoom: 1.5,
    });

    // Build geojson
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
          group: p.top_group,
          countryCode: p.country,
        },
      }))
    };

    // Add font and layers
    const onLoad = () => {
      map.addSource('heatmap-source', { type: 'geojson', data: geojson });

      map.addLayer({
        id: 'heatmap-layer',
        type: 'heatmap',
        source: 'heatmap-source',
        paint: {
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'weight'], 0, 0, 100, 1],
          'heatmap-intensity': 1,
          'heatmap-color': [
            'interpolate', ['linear'], ['heatmap-density'],
            0, 'rgba(0,0,255,0)',
            0.4, 'royalblue',
            0.6, 'cyan',
            0.8, 'lime',
            1, 'red'
          ],
          'heatmap-radius': 20,
        },
      });

      map.addLayer({
        id: 'point-layer',
        type: 'circle',
        source: 'heatmap-source',
        paint: {
          'circle-radius': [
            'interpolate', ['linear'], ['get', 'weight'],
            0, 10,
            100, 20,
            1000, 40
          ],
          'circle-color': 'rgba(255, 0, 0, 0.5)',
          'circle-opacity': 0.7,
          'circle-blur': 0.6,
        },
      });
    };

    // Popup variable
    let popup: mapboxgl.Popup;

    // Click and hover handlers
    const onMouseEnter = (e: mapboxgl.MapLayerMouseEvent) => {
      map.getCanvas().style.cursor = 'pointer';
      const feature = e.features![0];
      const coords = (feature.geometry as any).coordinates as [number, number];
      const props = feature.properties as any;
      const html = `
        <div style="text-align:center">
          <strong>${props.name}</strong><br/>
          Attacks: ${props.weight}<br/>
          Group: ${props.group}
        </div>`;
      popup = new mapboxgl.Popup({ closeButton: false, closeOnClick: false })
        .setLngLat(coords)
        .setHTML(html)
        .addTo(map);
    };

    const onMouseLeave = () => {
      map.getCanvas().style.cursor = '';
      if (popup) popup.remove();
    };

    const onClick = (e: mapboxgl.MapLayerMouseEvent) => {
      const props = (e.features![0].properties as any);
      openModal(props.countryCode);
    };

    // Subscibe to events
    map.on('load', onLoad);
    map.on('mouseenter', 'point-layer', onMouseEnter);
    map.on('mouseleave', 'point-layer', onMouseLeave);
    map.on('click', 'point-layer', onClick);

    // Cleanup
    return () => {
      map.off('load', onLoad);
      map.off('mouseenter', 'point-layer', onMouseEnter);
      map.off('mouseleave', 'point-layer', onMouseLeave);
      map.off('click', 'point-layer', onClick);
      map.remove();
    };
  }, [data]);

  if (loading) return <Loading message="Loading" />;
  
  if (error) return <ErrorDisplay message={error.message} />;

  return (
    <section aria-label="Heatmap attacks" className="bg-[#1a1a1a] text-gray-500 h-screen flex flex-col">
      <header className="p-4">
        <h1 className="text-2xl text-amber-50 font-bold text-center">
          Heatmap of ransomware attacks
        </h1>
      </header>
      <div
        ref={mapContainerRef}
        className="w-[90%] h-[80vh] rounded-lg shadow-lg p-3 mx-auto"
      />
    </section>
  );
};
