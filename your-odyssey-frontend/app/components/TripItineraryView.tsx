import React from 'react';
import styles from './TripItineraryView.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarker, faClock, faDollarSign, faStar } from '@fortawesome/free-solid-svg-icons';

interface Props {
  itinerary: any;
  showDayByDay?: boolean;
}

export default function TripItineraryView({ itinerary, showDayByDay = true }: Props) {
  if (!itinerary) return <div>No itinerary data</div>;

  const renderMaybe = (value: any) => {
    if (value === null || value === undefined) return null;
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') return String(value);
    if (Array.isArray(value)) return value.map((v, i) => <div key={i}>{renderMaybe(v)}</div>);
    // objects -> render as friendly key/value list
    if (typeof value === 'object') return renderObjectAsList(value);
    return String(value);
  };

  const formatKey = (k: string) => k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

  const renderObjectAsList = (obj: Record<string, any>) => {
    if (!obj || Object.keys(obj).length === 0) return null;
    return (
      <div className={styles.objectList}>
        {Object.entries(obj).map(([k, v]) => (
          <div key={k} className={styles.objectRow}>
            <strong>{formatKey(k)}:</strong> <span className={styles.objectValue}>{renderMaybe(v)}</span>
          </div>
        ))}
      </div>
    );
  };

  const renderDestinationInfo = (info: any) => {
    if (!info) return null;
    // Show prioritized info first (e.g., important_phrases)
    const priorityKeys = ['important_phrases', 'transportation', 'top_attractions'];
    const priorityItems: Record<string, any> = {};
    const others: Record<string, any> = {};
    Object.keys(info).forEach(k => {
      if (priorityKeys.includes(k)) priorityItems[k] = info[k];
      else others[k] = info[k];
    });

    return (
      <>
        {Object.keys(priorityItems).length > 0 && (
          <div className={styles.priorityList}>
            {Object.entries(priorityItems).map(([k, v]) => (
              <div key={k}>
                <strong>{formatKey(k)}:</strong>
                {Array.isArray(v) ? (
                  <ul>
                    {v.map((it: any, idx: number) => <li key={idx}>{renderMaybe(it)}</li>)}
                  </ul>
                ) : (
                  <div>{renderMaybe(v)}</div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className={styles.infoGrid}>
          {others.name && <div><strong>Name:</strong> {renderMaybe(others.name)}</div>}
          {others.language && <div><strong>Language:</strong> {renderMaybe(others.language)}</div>}
          {others.currency && <div><strong>Currency:</strong> {renderMaybe(others.currency)}</div>}
          {others.best_time_to_visit && <div><strong>Best time to visit:</strong> {renderMaybe(others.best_time_to_visit)}</div>}
          {others.cultural_tips && <div><strong>Cultural tips:</strong> {renderMaybe(others.cultural_tips)}</div>}
        </div>
      </>
    );
  };

  const renderPracticalInfo = (info: any) => {
    if (!info) return null;
  // Known fields in two-column grid
    const known = {} as Record<string, any>;
    ['timezone', 'voltage', 'emergency_numbers', 'health_advice'].forEach(k => {
      if (info[k] !== undefined) known[k] = info[k];
    });

    // Remaining fields
    const others: Record<string, any> = {};
    Object.keys(info).forEach(k => { if (!known.hasOwnProperty(k)) others[k] = info[k]; });

    // Prioritize emergency and transportation lists first
    const priorityKeys = ['emergency_numbers', 'important_phrases', 'transportation'];
    const priorityItems: Record<string, any> = {};
    const rest: Record<string, any> = {};
    Object.keys(info).forEach(k => {
      if (priorityKeys.includes(k)) priorityItems[k] = info[k];
      else if (!known.hasOwnProperty(k)) rest[k] = info[k];
    });

    return (
      <>
        {Object.keys(priorityItems).length > 0 && (
          <div className={styles.priorityList}>
            {Object.entries(priorityItems).map(([k, v]) => (
              <div key={k}>
                <strong>{formatKey(k)}:</strong>
                {Array.isArray(v) ? (
                  <ul>
                    {v.map((it: any, idx: number) => <li key={idx}>{renderMaybe(it)}</li>)}
                  </ul>
                ) : (
                  <div>{renderMaybe(v)}</div>
                )}
              </div>
            ))}
          </div>
        )}

        <div className={styles.infoGrid}>
          {Object.entries(known).map(([k, v]) => (
            <div key={k}><strong>{formatKey(k)}:</strong> {renderMaybe(v)}</div>
          ))}
        </div>

        {Object.keys(rest).length > 0 && (
          <div className={styles.fullWidth}>
            {renderObjectAsList(rest)}
          </div>
        )}
      </>
    );
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h3 className={styles.destination}>{renderMaybe(itinerary.destination)}</h3>
        <div className={styles.sub}>Duration: {renderMaybe(itinerary.duration)} days</div>
      </header>

      {itinerary.destination_info && (
        <section className={styles.section}>
          <h4>About the destination</h4>
          {renderDestinationInfo(itinerary.destination_info)}
        </section>
      )}

      {Array.isArray(itinerary.days) && (
        <section className={styles.section}>
          <h4>Day-by-day plan</h4>
          <div className={styles.days}>
            {itinerary.days.map((day: any) => (
              <article className={styles.dayCard} key={day.day}>
                <div className={styles.dayHeader}>
                  <div className={styles.dayTitle}>{renderMaybe(day.date)} — Day {renderMaybe(day.day)}: {renderMaybe(day.theme)}</div>
                </div>

                <div className={styles.activities}>
                  {Array.isArray(day.activities) && day.activities.map((act: any, idx: number) => (
                    <div className={styles.activity} key={idx}>
                      <div className={styles.activityRow}>
                        <div className={styles.activityName}>{renderMaybe(act.name)}</div>
                        <div className={styles.activityMeta}>
                          <span className={styles.metaItem}><FontAwesomeIcon icon={faMapMarker} /> {renderMaybe(act.location)}</span>
                          <span className={styles.metaItem}><FontAwesomeIcon icon={faClock} /> {renderMaybe(act.duration)}</span>
                          <span className={styles.metaItem}><FontAwesomeIcon icon={faDollarSign} /> {renderMaybe(act.estimated_cost)}</span>
                          {act.rating && <span className={styles.metaItem}><FontAwesomeIcon icon={faStar} /> {renderMaybe(act.rating)}</span>}
                        </div>
                      </div>
                      <div className={styles.activityDesc}>{renderMaybe(act.description)}</div>
                      {act.tips && <div className={styles.tips}>Tips: {renderMaybe(act.tips)}</div>}
                    </div>
                  ))}
                </div>

                {day.transportation_notes && <div className={styles.transport}>Transport: {renderMaybe(day.transportation_notes)}</div>}
              </article>
            ))}
          </div>
        </section>
      )}

      {itinerary.practical_info && (
        <section className={styles.section}>
          <h4>Practical info</h4>
          {renderPracticalInfo(itinerary.practical_info)}
        </section>
      )}
    </div>
  );
}
