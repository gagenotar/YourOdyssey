import { useState } from 'react';
import type { FormEvent } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons';
import { api } from '../services/api';
import ToastMessage from '../components/ToastMessage';
import type { GenerateItineraryResponse } from '../services/api';

import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Header } from './plan/Header';
import { TripPlanningForm } from './plan/TripPlanningForm';
import { TravelQA } from './plan/TravelQA';
import { ItineraryDisplay } from './plan/ItineraryDisplay';
import { useAuth0 } from '@auth0/auth0-react';
import styles from './plan.module.css';

export default function Plan() {
  const { getAccessTokenSilently, isAuthenticated, loginWithRedirect } = useAuth0();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [itinerary, setItinerary] = useState<GenerateItineraryResponse | null>(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [askingQuestion, setAskingQuestion] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [destination, setDestination] = useState("");
  const locationObj = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(locationObj.search);
    const dest = params.get("destination") || "";
    if (dest) setDestination(dest);
  }, [locationObj.search]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setItinerary(null);

    const formData = new FormData(e.currentTarget);
    try {
      const response = await api.generateItinerary({
        destination: formData.get('destination') as string,
        duration: parseInt(formData.get('duration') as string),
        budget: formData.get('budget') as string,
        preferences: formData.get('preferences') as string
      });
      console.log('API response:', response);
      setItinerary(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate itinerary');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    setAskingQuestion(true);
    setError(null);
    setAnswer(null);

    try {
      const response = await api.askQuestion({ question });
      setAnswer(response.answer);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get answer');
    } finally {
      setAskingQuestion(false);
    }
  };

  const handleExport = () => {
    if (!itinerary) return;
    const text = JSON.stringify(itinerary, null, 2);
    const blob = new Blob([text], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'travel-itinerary.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleSave = async () => {
    if (!itinerary) return;
    if (!isAuthenticated) {
      // prompt user to login
      if (confirm('You need to be logged in to save a trip. Log in now?')) {
        await loginWithRedirect();
      }
      return;
    }

    try {
      const audience = import.meta.env.VITE_AUTH0_AUDIENCE;
      const token = await getAccessTokenSilently(audience ? { authorizationParams: { audience } } : undefined);

      const res = await api.saveItinerary(itinerary.itinerary, token);
      // show temporary toast confirmation
      if (res.success) {
        setToastMessage('Saved itinerary');
      } else {
        setToastMessage('Failed to save itinerary');
      }
    } catch (err) {
      // If token/audience mismatch, prompt user to re-login and check env config
      const msg = err instanceof Error ? err.message : 'Failed to save itinerary';
      if (typeof msg === 'string' && msg.toLowerCase().includes('401')) {
        if (confirm('Authentication failed when saving. Re-login now?')) {
          await loginWithRedirect();
        }
      } else {
  setToastMessage(msg);
      }
    }
  };

  return (
    <div className={styles.mainContainer}>
      <Header />
      <div className={styles.content}>
        <TripPlanningForm 
          onSubmit={handleSubmit}
          loading={loading}
          initialDestination={destination}
          setDestination={setDestination}
        />
        <TravelQA 
          question={question}
          onQuestionChange={(value) => setQuestion(value)}
          onAskQuestion={handleAskQuestion}
          answer={answer}
          askingQuestion={askingQuestion}
        />
        {/* Loading State */}
        {loading && (
          <div className={styles.loadingContainer}>
            <div className={styles.loadingSpinner}></div>
            <p>
              Searching for the best travel information and creating your personalized itinerary...
            </p>
          </div>
        )}
        {/* Error Message */}
        {error && (
          <div className={styles.errorContainer}>
            <FontAwesomeIcon icon={faExclamationCircle} />
            <div>{error}</div>
          </div>
        )}
        {/* Itinerary Results */}
        {itinerary && (
          <ItineraryDisplay 
            itinerary={itinerary}
            onExport={handleExport}
            onSave={handleSave}
            isAuthenticated={isAuthenticated}
            onLogin={() => loginWithRedirect()}
          />
        )}
        {toastMessage && (
          <ToastMessage message={toastMessage} onClose={() => setToastMessage(null)} />
        )}
      </div>
    </div>
  );
}

function formatAnswer(answer: string): string {
  return answer
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^\s*/, '<p>')
    .replace(/\s*$/, '</p>');
}
