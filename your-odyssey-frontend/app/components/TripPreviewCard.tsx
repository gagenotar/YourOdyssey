import React from 'react';
import styles from './TripPreviewCard.module.css';

interface Props {
  item: any;
  onClick?: (item: any) => void;
}

export default function TripPreviewCard({ item, onClick }: Props) {
  const itinerary = item.itinerary || {};
  const title = itinerary.destination || itinerary.destination_info?.name || 'Trip';
  const location = itinerary.destination_info?.name || '';

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.key === 'Enter' || e.key === ' ') && onClick) {
      e.preventDefault();
      onClick(item);
    }
  };

  return (
    <article
      className={styles.cardList}
      onClick={() => onClick && onClick(item)}
      role="button"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-label={`Open trip ${title}`}
    >
      <div className={styles.content}>
        <div className={styles.rowTop}>
          <h3 className={styles.title} title={title}>{title}</h3>
          <div className={styles.meta}>{new Date(item.created_at).toLocaleDateString()}</div>
        </div>

        {location && <div className={styles.location}>{location}</div>}

        <div className={styles.actions}>
          <button
            type="button"
            className="btn btn-sm btn-outline-primary"
            onClick={(e) => { e.stopPropagation(); onClick && onClick(item); }}
            aria-label={`View details for ${title}`}
          >
            View
          </button>
        </div>
      </div>
    </article>
  );
}
