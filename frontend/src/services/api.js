import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
});

export const createSession = async () => {
  const res = await api.post('/session/create');
  return res.data.session_id;
};

export const sendQuery = async (session_id, query) => {
  const res = await api.post('/query', { session_id, query });
  return res.data;
};

export const getHistory = async (session_id) => {
  const res = await api.get(`/session/${session_id}/history`);
  return res.data;
};

export const triggerIngest = async () => {
  const res = await api.post('/ingest');
  return res.data;
};

export const getPipelineStats = async () => {
  const res = await api.get('/admin/pipeline');
  return res.data;
};

export const getHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};
