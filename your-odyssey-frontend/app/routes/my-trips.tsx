import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { api } from '../services/api';
import TripPreviewCard from '../components/TripPreviewCard';
import TripDetailModal from '../components/TripDetailModal';

export default function MyTrips() {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [bio, setBio] = useState<string>('');
  const [bioLoading, setBioLoading] = useState(false);
  const [bioSaving, setBioSaving] = useState(false);
  const [editingBio, setEditingBio] = useState(false);
  const [draftBio, setDraftBio] = useState('');
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<any | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const load = async () => {
      if (!isAuthenticated) return;
      setLoading(true);
      try {
        const token = await getAccessTokenSilently();
        const res = await api.listSavedItineraries(token);
        setItems(res.items || []);
      } catch (err) {
        console.error('Failed to load saved trips', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [isAuthenticated, getAccessTokenSilently]);

  // load profile bio
  useEffect(() => {
    const loadProfile = async () => {
      if (!isAuthenticated) return;
      setBioLoading(true);
      try {
        const token = await getAccessTokenSilently();
        const p = await api.getProfile(token);
        setBio((p.profile && p.profile.bio) || '');
      } catch (err) {
        console.error('Failed to load profile', err);
      } finally {
        setBioLoading(false);
      }
    };
    loadProfile();
  }, [isAuthenticated, getAccessTokenSilently]);

  const openDetail = (item: any) => {
    setSelected(item);
    setShowModal(true);
  };

  return (
    <div className="container py-4">
      <h1>My Trips</h1>
      <div className="mb-4">
        <h5>Your bio</h5>
        {bioLoading ? (
          <div className="text-muted">Loading bio…</div>
        ) : (
          <div>
            {!editingBio ? (
              <div className="d-flex align-items-start gap-3">
                <div className="flex-grow-1">
                  {bio ? (
                    <div style={{whiteSpace: 'pre-wrap'}}>{bio}</div>
                  ) : (
                    <div className="text-muted">You haven't added a bio yet.</div>
                  )}
                </div>
                <div>
                  <button className="btn btn-link" onClick={() => { setDraftBio(bio); setEditingBio(true); }}>Edit</button>
                </div>
              </div>
            ) : (
              <div>
                <textarea className="form-control mb-2" rows={4} value={draftBio} onChange={e => setDraftBio(e.target.value)} />
                <div className="d-flex gap-2">
                  <button className="btn btn-primary" disabled={bioSaving} onClick={async () => {
                    setBioSaving(true);
                    try {
                      const token = await getAccessTokenSilently();
                      await api.saveProfile(draftBio, token);
                      setBio(draftBio);
                      setEditingBio(false);
                    } catch (err) {
                      console.error('Failed to save bio', err);
                    } finally {
                      setBioSaving(false);
                    }
                  }}>{bioSaving ? 'Saving…' : 'Save'}</button>
                  <button className="btn btn-secondary" onClick={() => { setDraftBio(bio); setEditingBio(false); }}>Cancel</button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      {loading && (
        <div className="d-flex align-items-center gap-2 my-3">
          <div className="spinner-border text-primary" role="status" aria-hidden="true"></div>
          <div>Loading your saved trips…</div>
        </div>
      )}
      {!isAuthenticated && <div className="alert alert-info">Please log in to see your saved trips.</div>}

      <div className="list-group">
        {items.length === 0 && !loading && isAuthenticated && (
          <div className="p-4 border rounded bg-light text-center">You don't have any saved trips yet. Start planning to see them here.</div>
        )}

        {items.map((item, idx) => (
          <div key={item.id} className="mb-2">
            <TripPreviewCard item={item} onClick={openDetail} />
            {idx < items.length - 1 && <div style={{height: 8}} />}
          </div>
        ))}
      </div>

      <TripDetailModal show={showModal} item={selected} onClose={() => setShowModal(false)} />
    </div>
  );
}
