import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import TripPreviewCard from '../components/TripPreviewCard';
import TripDetailModal from '../components/TripDetailModal';

export default function FollowedProfile() {
  const { id } = useParams();
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [profile, setProfile] = useState<any | null>(null);
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<any | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const load = async () => {
      if (!isAuthenticated) return;
      setLoading(true);
      try {
        let usedAuthProfile = false;
        let usedAuthTrips = false;

        // Dev data will be a fallback; fetch it first so there's no empty flicker.
        try {
          const pDev = await fetch(`http://localhost:5000/dev/users/${id}`);
          if (pDev.ok) {
            const pd = await pDev.json();
            setProfile(pd.user || pd);
          }
          const tDev = await fetch(`http://localhost:5000/dev/users/${id}/saved_trips`);
          if (tDev.ok) {
            const td = await tDev.json();
            setItems(td.items || []);
          }
        } catch (err) {
          // ignore dev fetch errors and try auth below
        }

        if (isAuthenticated) {
          try {
            const token = await getAccessTokenSilently();
            const pRes = await fetch(`http://localhost:5000/users/${id}`, { headers: { Authorization: `Bearer ${token}` } });
            if (pRes.ok) {
              const pd = await pRes.json();
              if (pd.user) { setProfile(pd.user); usedAuthProfile = true; }
            }

            const tRes = await fetch(`http://localhost:5000/users/${id}/saved_trips`, { headers: { Authorization: `Bearer ${token}` } });
            if (tRes.ok) {
              const td = await tRes.json();
              if (Array.isArray(td.items) && td.items.length > 0) { setItems(td.items); usedAuthTrips = true; }
            }
          } catch (err) {
            console.warn('Auth fetch failed, keeping dev data', err);
          }
        }
      } catch (err) {
        console.error('Failed to load profile trips', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) load();
  }, [id, isAuthenticated, getAccessTokenSilently]);

  const openDetail = (item: any) => {
    setSelected(item);
    setShowModal(true);
  };

  if (!isAuthenticated) return <div className="container py-4">Please log in to view this profile.</div>;

  return (
    <div className="container py-4">
      <div style={{display:'flex',alignItems:'center',gap:16}}>
        {profile?.picture && <img src={profile.picture} alt="avatar" style={{width:64,height:64,borderRadius:32}} />}
        <div>
          <h2>{profile?.name || profile?.username || `User ${id}`}</h2>
          <div style={{color:'#6b7280'}}>{profile?.bio}</div>
        </div>
      </div>

      <hr />

      <h4>Saved Trips</h4>

      {loading && <div className="d-flex align-items-center gap-2 my-3"><div className="spinner-border text-primary" role="status" aria-hidden="true"></div><div>Loading trips…</div></div>}

      <div className="list-group mt-3">
        {items.length === 0 && !loading && (
          <div className="p-3 border rounded bg-light">No saved trips found for this user.</div>
        )}

        {items.map((item:any, idx:number) => (
          <div key={item.id} className="mb-2">
            <TripPreviewCard item={item} onClick={openDetail} />
          </div>
        ))}
      </div>

      <TripDetailModal show={showModal} item={selected} onClose={() => setShowModal(false)} />
    </div>
  );
}
