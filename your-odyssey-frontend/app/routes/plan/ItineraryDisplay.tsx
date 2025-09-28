import type { GenerateItineraryResponse, DayPlan } from '../../services/api';
import React, { Suspense, lazy, useState, useMemo } from 'react';

const DayMap = lazy(() => import('../../components/DayMap'));
import styles from './ItineraryDisplay.module.css';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import { Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faMapMarkedAlt, 
  faDownload, 
  faClock, 
  faMapMarker, 
  faDollarSign, 
  faStar 
} from '@fortawesome/free-solid-svg-icons';

interface ItineraryDisplayProps {
  itinerary: GenerateItineraryResponse;
  onExport: () => void;
  onSave?: () => void;
  isAuthenticated?: boolean;
  onLogin?: () => void;
}

export function ItineraryDisplay({ itinerary, onExport, onSave, isAuthenticated, onLogin }: ItineraryDisplayProps) {
  console.log('ItineraryDisplay props:', itinerary);
  const trip = itinerary.itinerary;
  const [selectedDayIndex, setSelectedDayIndex] = useState(0);

  const days = Array.isArray(trip?.days) ? trip.days : [];
  const selectedDay = days[selectedDayIndex] ?? null;

  return (
    <div className={`${styles.itineraryContainer} container`}>
      <div className={styles.header}>
        <h2 className={styles.title}>
          <FontAwesomeIcon icon={faMapMarkedAlt} />
          Your Personalized Itinerary
        </h2>
        <div className={styles.controlGroup}>
          <button onClick={onExport} className={styles.exportButton}>
          <FontAwesomeIcon icon={faDownload} />
          Export
        </button>
          {typeof onSave === 'function' && (
            isAuthenticated ? (
              <button onClick={onSave} className={`${styles.exportButton} btn-secondary ms-2`}>
                Save
              </button>
            ) : (
              <OverlayTrigger
                placement="top"
                overlay={<Tooltip id={`tooltip-disabled`}>Log in to save this itinerary</Tooltip>}
              >
                <span className={styles.disabledWrapper}>
                  <button
                    disabled
                    className={`${styles.exportButtonDisabled} ms-2`}
                    aria-disabled="true"
                  >
                    Save
                  </button>
                </span>
              </OverlayTrigger>
            )
          )}
        </div>
      </div>

      <div className={styles.destination}>
        <h3 className={styles.destinationTitle}>{trip?.destination}</h3>
        <p>{trip?.duration} days of amazing experiences</p>
      </div>

      <div className={styles.twoColumn} style={{ display: 'flex', gap: 16 }}>
        <div className={styles.leftColumn} style={{ flex: '0 0 380px' }}>
          {days.map((day: DayPlan, idx: number) => (
            <div
              key={day.day}
              className={`${styles.dayCard} ${idx === selectedDayIndex ? styles.selectedDay : ''}`}
              onClick={() => setSelectedDayIndex(idx)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setSelectedDayIndex(idx); }}
            >
              <div className={styles.dayHeader}>
                <h3 className={styles.dayTitle}>
                  {day.date} - {day.theme}
                </h3>
                {day.transportation_notes && (
                  <p className={styles.transportNote}>
                    {day.transportation_notes}
                  </p>
                )}
              </div>

              <div className={styles.activities}>
                {Array.isArray(day.activities) && day.activities.map((activity, index) => (
                  <div key={index} className={styles.activity}>
                    <div className={styles.activityHeader}>
                      <h4 className={styles.activityName}>{activity.name}</h4>
                      <span className={styles.activityCategory}>
                        {activity.category}
                      </span>
                    </div>

                    <p>{activity.description}</p>

                    <div className={styles.activityDetails}>
                      <div className={styles.activityInfo}>
                        <FontAwesomeIcon icon={faMapMarker} />
                        {activity.location}
                      </div>
                      <div className={styles.activityInfo}>
                        <FontAwesomeIcon icon={faClock} />
                        {activity.duration}
                      </div>
                      <div className={styles.activityInfo}>
                        <FontAwesomeIcon icon={faDollarSign} />
                        {activity.estimated_cost}
                      </div>
                      {activity.rating && (
                        <div className={styles.activityInfo}>
                          <FontAwesomeIcon icon={faStar} />
                          {activity.rating}
                        </div>
                      )}
                    </div>

                    {activity.opening_hours && (
                      <div className={styles.openingHours}>
                        Hours: {activity.opening_hours}
                      </div>
                    )}

                    {activity.tips && (
                      <div className={styles.tips}>
                        {activity.tips}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className={styles.dailyBudget}>
                Daily Budget: {day.total_estimated_cost}
              </div>
            </div>
          ))}
        </div>

        <div className={styles.rightColumn} style={{ flex: '1 1 auto' }}>
          <Suspense fallback={<div>Loading map…</div>}>
            <DayMap addresses={(selectedDay?.activities ?? []).map((a:any) => a.location).filter(Boolean)} height={600} />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
