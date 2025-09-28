import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import { api } from '../services/api';
import styles from '../components/TripPreviewCard.module.css';

export default function Follows() {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [follows, setFollows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        // Try auth fetch first; if it returns a successful non-empty result, use it.
        let usedAuth = false;
        if (isAuthenticated) {
          try {
            const token = await getAccessTokenSilently();
            const res = await fetch('http://localhost:5000/follows', { headers: { Authorization: `Bearer ${token}` } });
            if (res.ok) {
              const d = await res.json();
              if (Array.isArray(d.items) && d.items.length > 0) {
                setFollows(d.items);
                usedAuth = true;
              }
            }
          } catch (err) {
            console.warn('Auth fetch failed, will try dev endpoint', err);
          }
        }

        if (!usedAuth) {
          const devRes = await fetch('http://localhost:5000/dev/follows');
          if (devRes.ok) {
            const dd = await devRes.json();
            setFollows(dd.items || []);
          }
        }
      } catch (err) {
        console.error('Failed to load follows', err);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [isAuthenticated, getAccessTokenSilently]);

  if (!isAuthenticated) return <div className="container py-4">Please log in to view follows.</div>;

  return (
    <div className="container py-4">
      <h1>People you follow</h1>

      {loading && <div className="d-flex align-items-center gap-2 my-3"><div className="spinner-border text-primary" role="status" aria-hidden="true"></div><div>Loading…</div></div>}

      {follows.length === 0 && !loading && (
        <div className="p-4 border rounded bg-light">You are not following anyone yet.</div>
      )}

      <div className="mt-3">
        {follows.map((p: any, idx: number) => (
          <div key={p.id} className="mb-2">
            <Link to={`/follows/${p.followed_id}`} className={styles.cardList}>
              <div className={styles.content}>
                <div className={styles.rowTop}>
                  <h3 className={styles.title} style={{margin:0}}>{p.name || p.username}</h3>
                  <div className={styles.meta}>{p.username ? `@${p.username}` : ''}</div>
                </div>

                {p.bio && <div className={styles.location}>{p.bio}</div>}

                <div className={styles.actions}>
                  <div style={{fontSize:'0.9rem', color:'#6b7280'}}>View trips →</div>
                </div>
              </div>
            </Link>
            {idx < follows.length - 1 && <div style={{height: 8}} />}
          </div>
        ))}
      </div>
    </div>
  );
}
