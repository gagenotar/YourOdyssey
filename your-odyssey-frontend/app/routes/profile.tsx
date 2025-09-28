import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { api } from '../services/api';

export default function Profile() {
  const { getAccessTokenSilently, isAuthenticated, user } = useAuth0();
  const [me, setMe] = useState<any | null>(null);
  const [tripsCount, setTripsCount] = useState<number | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!isAuthenticated) return;
      try {
        const token = await getAccessTokenSilently();
        const [meRes, tripsRes] = await Promise.all([
          fetch('http://localhost:5000/me', { headers: { Authorization: `Bearer ${token}` } }),
          fetch('http://localhost:5000/saved_trips', { headers: { Authorization: `Bearer ${token}` } })
        ]);

        if (meRes.ok) {
          const d = await meRes.json();
          setMe(d.user);
        }
        if (tripsRes.ok) {
          const d2 = await tripsRes.json();
          setTripsCount((d2.items || []).length);
        }
      } catch (err) {
        console.error('Failed to load profile', err);
      }
    };

    load();
  }, [isAuthenticated, getAccessTokenSilently]);

  if (!isAuthenticated) {
    return <div className="container py-4">Please log in to view your profile.</div>;
  }

  return (
    <div className="container py-4">
      <h1>Profile</h1>
      <div className="card mb-4">
        <div className="card-body d-flex align-items-center">
          {me?.picture && <img src={me.picture} alt="avatar" style={{width:64,height:64,borderRadius:32,marginRight:16}} />}
          <div>
            <h4>{me?.name || user?.name}</h4>
            <div>{me?.email || user?.email}</div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <h5>Saved Trips</h5>
          <div>{tripsCount === null ? 'Loading...' : `${tripsCount} saved trips`}</div>
          <div className="mt-3">
            <a href="/my-trips" className="btn btn-primary">View My Trips</a>
          </div>
        </div>
      </div>
    </div>
  );
}
