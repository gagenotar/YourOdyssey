import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlane } from '@fortawesome/free-solid-svg-icons';
import styles from './Header.module.css';

export function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <h1 className={styles.title}>
          <FontAwesomeIcon icon={faPlane} />
          AI Travel Itinerary Planner
        </h1>
        <p className={styles.subtitle}>
          Powered by Gemini 2.0 Flash with Real-time Google Search
        </p>
      </div>
    </header>
  );
}
