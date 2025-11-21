import axios from 'axios';

const API_BASE_URL = import.meta.env.PROD ? '/api' : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Model info
  getModelInfo: async () => {
    const response = await api.get('/model/info');
    return response.data;
  },

  // Rasmni yuklash va bashorat qilish
  predictImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Batch prediction
  predictBatch: async (files) => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    const response = await api.post('/predict/batch', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Tarixni olish
  getHistory: async () => {
    const response = await api.get('/history');
    return response.data;
  },

  // Tarixni tozalash
  clearHistory: async () => {
    const response = await api.delete('/history');
    return response.data;
  },
};

export default api;
