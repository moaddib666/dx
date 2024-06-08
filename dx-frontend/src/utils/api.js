import axios from 'axios';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 1000,
});

export const registerUser = async (username, email, password) => {
  const response = await api.post('/register', { username, email, password });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await api.post('/login', { email, password });
  return response.data;
};

export default api;
