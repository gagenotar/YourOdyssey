// API service for connecting to the Flask backend

const API_BASE_URL = 'http://localhost:5000';

export interface GenerateItineraryRequest {
  destination: string;
  duration: number;
  preferences: string;
  budget: string;
}

export interface Activity {
  name: string;
  description: string;
  location: string;
  duration: string;
  estimated_cost: string;
  category: string;
  rating?: number;
  opening_hours?: string;
  tips?: string;
}

export interface DayPlan {
  day: number;
  date: string;
  theme: string;
  activities: Activity[];
  total_estimated_cost: string;
  transportation_notes?: string;
}

export interface ItineraryObject {
  days: DayPlan[];
  destination: string;
  duration: number;
  destination_info?: any;
  outbound_transport?: any;
  // add other fields as needed
}

export interface GenerateItineraryResponse {
  success: boolean;
  itinerary: ItineraryObject;
}

export interface AskQuestionRequest {
  question: string;
}

export interface AskQuestionResponse {
  success: boolean;
  answer: string;
}

export const api = {
  async generateItinerary(request: GenerateItineraryRequest): Promise<GenerateItineraryResponse> {
    const response = await fetch(`${API_BASE_URL}/generate_itinerary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to generate itinerary');
    }

    return response.json();
  },

  async askQuestion(request: AskQuestionRequest): Promise<AskQuestionResponse> {
    const response = await fetch(`${API_BASE_URL}/ask_question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get answer');
    }

    return response.json();
  },

  async checkHealth(): Promise<{ status: string; model: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return response.json();
  },

  async saveItinerary(itinerary: ItineraryObject, accessToken?: string): Promise<{ success: boolean; id?: number }>{
    const headers: Record<string,string> = { 'Content-Type': 'application/json' };
    if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

    const response = await fetch(`${API_BASE_URL}/saved_trips`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ itinerary }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to save itinerary');
    }

    return response.json();
  },

  async listSavedItineraries(accessToken?: string): Promise<{ success: boolean; items?: any[] }>{
    const headers: Record<string,string> = {};
    if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

    const response = await fetch(`${API_BASE_URL}/saved_trips`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to list itineraries');
    }

    return response.json();
  }
,

  async getProfile(accessToken?: string): Promise<{ success: boolean; profile?: any }>{
    const headers: Record<string,string> = { 'Content-Type': 'application/json' };
    if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'GET',
      headers
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get profile');
    }

    return response.json();
  },

  async saveProfile(bio: string, accessToken?: string): Promise<{ success: boolean }>{
    const headers: Record<string,string> = { 'Content-Type': 'application/json' };
    if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ bio })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to save profile');
    }

    return response.json();
  }
}
