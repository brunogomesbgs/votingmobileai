import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error);

    // Handle network errors
    if (!error.response) {
      throw new Error('Network error. Please check your connection.');
    }

    // Handle HTTP errors
    const { status, data } = error.response;
    const errorMessage = data?.detail || data?.error || 'An error occurred';

    switch (status) {
      case 400:
        throw new Error(errorMessage);
      case 404:
        throw new Error(errorMessage);
      case 409:
        throw new Error(errorMessage);
      case 500:
        throw new Error('Server error. Please try again later.');
      default:
        throw new Error(errorMessage);
    }
  }
);

export const apiService = {
  // Create a new feature
  createFeature: async (featureData) => {
    try {
      const response = await apiClient.post('/features', featureData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get all features
  getFeatures: async () => {
    try {
      const response = await apiClient.get('/features');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get a specific feature
  getFeature: async (featureId) => {
    try {
      const response = await apiClient.get(`/features/${featureId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Vote for a feature
  voteFeature: async (voteData) => {
    try {
      const response = await apiClient.post('/votes', voteData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};