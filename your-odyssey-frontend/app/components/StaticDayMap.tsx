import React from 'react';

interface Props {
  addresses: string[];
  width?: number;
  height?: number;
  zoom?: number;
}

export default function StaticDayMap({ addresses, width = 800, height = 420, zoom = 12 }: Props) {
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
  if (!apiKey) {
    return <div style={{ color: 'red' }}>Google Maps API key not configured</div>;
  }

  // Build markers parameter by letting Static Maps geocode the address strings.
  // Keep URL length modest by limiting addresses if necessary.
  const safeAddresses = addresses.filter(Boolean).slice(0, 10);
  const markersParam = safeAddresses.map(a => `markers=${encodeURIComponent(a)}`).join('&');

  const sizeParam = `size=${Math.min(width, 640)}x${Math.min(height, 640)}`; // keep within common limits
  const url = `https://maps.googleapis.com/maps/api/staticmap?${markersParam}&${sizeParam}&zoom=${zoom}&key=${apiKey}`;

  // Link to a Google Maps search for the first address (if any)
  const mapsLink = safeAddresses.length ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(safeAddresses[0])}` : 'https://www.google.com/maps';

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <a href={mapsLink} target="_blank" rel="noreferrer" style={{ display: 'block' }}>
        <img src={url} alt={`Map of ${safeAddresses.join(', ')}`} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 8 }} />
      </a>
      {addresses.length > safeAddresses.length && (
        <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 6 }}>Only showing first {safeAddresses.length} locations</div>
      )}
    </div>
  );
}
