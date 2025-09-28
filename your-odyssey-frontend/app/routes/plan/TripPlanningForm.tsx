import React, { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkedAlt, faSpinner, faMagic } from '@fortawesome/free-solid-svg-icons';
import styles from './TripPlanningForm.module.css';


interface TripPlanningFormProps {
  onSubmit: (e: FormEvent<HTMLFormElement>) => Promise<void>;
  loading: boolean;
  initialDestination?: string;
  setDestination?: (dest: string) => void;
}

export function TripPlanningForm({ onSubmit, loading, initialDestination, setDestination }: TripPlanningFormProps) {
  const [destination, setDestinationState] = useState(initialDestination || "");
  useEffect(() => {
    if (typeof initialDestination !== "undefined") setDestinationState(initialDestination);
  }, [initialDestination]);

  return (
    <div className={`${styles.formContainer} container`}>
      <h2 className={styles.formTitle}>
        <FontAwesomeIcon icon={faMapMarkedAlt} />
        Plan Your Perfect Trip
      </h2>

      <form onSubmit={e => {
        if (setDestination) setDestination(destination);
        onSubmit(e);
      }}>
        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label htmlFor="destination">
              Destination *
            </label>
            <input
              type="text"
              id="destination"
              name="destination"
              placeholder="e.g., Paris, France"
              required
              className="form-control"
              value={destination}
              onChange={e => {
                setDestinationState(e.target.value);
                if (setDestination) setDestination(e.target.value);
              }}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="duration">
              Duration (days)
            </label>
            <select
              id="duration"
              name="duration"
              defaultValue="5"
              className="form-select"
            >
              <option value="3">3 days</option>
              <option value="5">5 days</option>
              <option value="7">7 days</option>
              <option value="10">10 days</option>
              <option value="14">14 days</option>
            </select>
          </div>
        </div>

        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label htmlFor="budget">
              Budget Range
            </label>
            <select
              id="budget"
              name="budget"
              defaultValue="moderate"
              className="form-select"
            >
              <option value="budget">Budget (Under $100/day)</option>
              <option value="moderate">Moderate ($100-250/day)</option>
              <option value="luxury">Luxury ($250+/day)</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="preferences">
              Travel Style
            </label>
            <select
              id="preferences"
              name="preferences"
              defaultValue="mix of everything"
              className="form-select"
            >
              <option value="cultural and historical">Cultural & Historical</option>
              <option value="adventure and outdoor">Adventure & Outdoor</option>
              <option value="food and nightlife">Food & Nightlife</option>
              <option value="relaxation and wellness">Relaxation & Wellness</option>
              <option value="family friendly">Family Friendly</option>
              <option value="mix of everything">Mix of Everything</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={styles.submitButton}
        >
          <FontAwesomeIcon icon={loading ? faSpinner : faMagic} spin={loading} />
          {loading ? 'Generating...' : 'Generate My Itinerary'}
        </button>
      </form>
    </div>
  );
}
