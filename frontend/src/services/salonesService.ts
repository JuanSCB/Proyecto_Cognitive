import api from '../api/axios';
import type { Salon } from '../types/api';

export const getSalones = () => api.get<Salon[]>('/api/salones').then(res => res.data);
export const createSalon = (payload: Partial<Salon>) => api.post<Salon>('/api/salones', payload).then(res => res.data);
export const updateSalon = (id: number, payload: Partial<Salon>) => api.put<Salon>(`/api/salones/${id}`, payload).then(res => res.data);
export const deleteSalon = (id: number) => api.delete(`/api/salones/${id}`).then(res => res.data);

export default {
  getSalones,
  createSalon,
  updateSalon,
  deleteSalon
};
