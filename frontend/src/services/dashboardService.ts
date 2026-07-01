import api from '../api/axios';
import type { DashboardSalon } from '../types/api';

export const getSalones = () => api.get<DashboardSalon[]>('/api/dashboard/salones').then(res => res.data);
export const getSalon = (id: string | number) => api.get(`/api/salones/${id}`).then(res => res.data);
export const analyzeRoom = (id: string | number) => api.post(`/api/ai/analyze-room/${id}`).then(res => res.data);

export default {
  getSalones,
  getSalon,
  analyzeRoom
};
