import { useEffect, useState } from 'react';
import { checkBackendHealth } from '../utils/api';

export function Welcome() {
  const [backendStatus, setBackendStatus] = useState<string>('Checking...');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await checkBackendHealth();
        setBackendStatus(response.message);
        setError('');
      } catch (err) {
        setBackendStatus('Offline');
        setError('Could not connect to the backend server');
      }
    };

    checkConnection();
  }, []);

  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <header className="flex flex-col items-center gap-9">
          <h1 className="text-4xl font-bold text-center">Hello, World!</h1>
        </header>
        <div className="max-w-[300px] w-full space-y-6 px-4">
          <p className="leading-6 text-gray-700 dark:text-gray-200 text-center">
            Welcome to your new React app.
          </p>
          <div className="text-center">
            <p className="font-semibold">Backend Status:</p>
            <p className={error ? 'text-red-500' : 'text-green-500'}>
              {error || backendStatus}
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
