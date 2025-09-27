interface HealthResponse {
  message: string;
}

export async function checkBackendHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch('http://localhost:8000/api/health/');
    if (!response.ok) {
      throw new Error('Backend server is not responding');
    }
    return await response.json();
  } catch (error) {
    throw new Error('Could not connect to the backend server');
  }
}
