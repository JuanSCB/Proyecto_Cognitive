import api from '../api/axios';
import type { Salon } from '../types/api';

export const getSalones = () => api.get<Salon[]>('/api/salones').then(res => res.data);
export const createSalon = (payload: Partial<Salon>) => api.post<Salon>('/api/salones', payload).then(res => res.data);
export const updateSalon = (id: number, payload: Partial<Salon>) => {
  // Diagnostic: log before calling axios.put (dev only)
  if (import.meta.env.DEV) {
    // eslint-disable-next-line no-console
    console.debug('[salonesService] updateSalon called', { id, payload });
    const stored = localStorage.getItem('iluminacion-auth');
    try {
      const token = stored ? JSON.parse(stored).token : null;
      // eslint-disable-next-line no-console
      console.debug('[salonesService] stored token present?', Boolean(token));
    } catch (e) {
      // eslint-disable-next-line no-console
      console.debug('[salonesService] error reading stored auth', e);
    }
  }
  return api.put<Salon>(`/api/salones/${id}`, payload).then(res => res.data);
};
export const deleteSalon = (id: number) => api.delete(`/api/salones/${id}`).then(res => res.data);

export default {
  getSalones,
  createSalon,
  updateSalon,
  deleteSalon
};
