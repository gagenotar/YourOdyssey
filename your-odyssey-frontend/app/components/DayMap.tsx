import React, { useEffect, useRef, useState } from 'react';

interface DayMapProps {
  addresses: string[];
  height?: number|string;
}

declare global {
  interface Window {
    initMap?: () => void;
    google: any;
  }
}

function loadGoogleMapsApi(apiKey: string) {
  return new Promise<void>((resolve, reject) => {
    if (typeof window === 'undefined') return reject(new Error('No window object'));
    if (window.google && window.google.maps) return resolve();

    const existing = document.getElementById('gmaps-script');
    if (existing) {
      existing.addEventListener('load', () => resolve());
      existing.addEventListener('error', () => reject(new Error('Failed to load Google Maps')));
      return;
    }

    const script = document.createElement('script');
    script.id = 'gmaps-script';
    script.async = true;
    script.defer = true;
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Google Maps script'));
    document.head.appendChild(script);
  });
}

export default function DayMap({ addresses, height = '100%' }: DayMapProps) {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    if (!key) {
      setError('Google Maps API key not configured');
      return;
    }
    let mounted = true;

    // initialize maps script and map instance if not already
    loadGoogleMapsApi(key)
      .then(() => {
        if (!mounted) return;
        if (mapInstanceRef.current) return; // already initialized
        if (!mapRef.current) return;

        const defaultCenter = { lat: 0, lng: 0 };
        mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
          center: defaultCenter,
          zoom: 12,
        });
      })
      .catch((err) => setError(err instanceof Error ? err.message : String(err)));

    return () => { mounted = false; };
  }, [addresses]);

  // separate effect: when addresses change and map is initialized, geocode and update markers
  useEffect(() => {
    if (!mapInstanceRef.current) return; // wait until map is initialized
    const geocoder = new window.google.maps.Geocoder();
    const bounds = new window.google.maps.LatLngBounds();

    // clear previous markers
    if (markersRef.current.length) {
      markersRef.current.forEach((m) => m.setMap(null));
      markersRef.current = [];
    }

    const addressPromises = addresses.map((addr, idx) => new Promise<void>((res) => {
      if (!addr) return res();
      geocoder.geocode({ address: addr }, (results: any, status: string) => {
        console.debug('[DayMap] geocode', { addr, status, results });
        if (status === 'OK' && results && results[0]) {
          const gLoc = results[0].geometry.location;
          const pos = { lat: typeof gLoc.lat === 'function' ? gLoc.lat() : gLoc.lat, lng: typeof gLoc.lng === 'function' ? gLoc.lng() : gLoc.lng };
          const marker = new window.google.maps.Marker({
            position: pos,
            map: mapInstanceRef.current,
            title: addr,
          });
          markersRef.current.push(marker);

          const info = new window.google.maps.InfoWindow({ content: `<div style="max-width:200px"><strong>${addr}</strong></div>` });
          marker.addListener('click', () => info.open({ anchor: marker, map: mapInstanceRef.current }));

          bounds.extend(pos);
        } else if (status === 'ZERO_RESULTS') {
          console.warn('[DayMap] geocode ZERO_RESULTS for', addr);
        } else if (status === 'OVER_QUERY_LIMIT') {
          console.warn('[DayMap] geocode OVER_QUERY_LIMIT; consider rate-limiting or server-side geocoding');
        } else {
          console.warn('[DayMap] geocode failed', { addr, status });
        }
        res();
      });
    }));

    Promise.all(addressPromises).then(() => {
      if (markersRef.current.length > 0) {
        try {
          mapInstanceRef.current.fitBounds(bounds);
        } catch (e) {
          console.debug('[DayMap] fitBounds failed', e);
        }
      } else {
        mapInstanceRef.current.setCenter({ lat: 0, lng: 0 });
        mapInstanceRef.current.setZoom(2);
      }
    });
  }, [addresses]);

  return (
    <div style={{ height: '100%' }}>
      {error ? <div style={{ color: 'red' }}>{error}</div> : null}
      <div
        ref={mapRef}
        style={{ width: '100%', height: height }}
        role="region"
        aria-label="Map of activities for this day"
      />
    </div>
  );
}
