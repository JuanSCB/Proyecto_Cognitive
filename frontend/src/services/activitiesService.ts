import api from '../api/axios';
import type { Actividad } from '../types/api';

export const getActivities = () => api.get<Actividad[]>('/api/actividades').then(res => res.data);
export const getActivity = (id: number) => api.get<Actividad>(`/api/actividades/${id}`).then(res => res.data);
export const createActivity = (payload: Actividad) => api.post<Actividad>('/api/actividades', payload).then(res => res.data);
export const updateActivity = (id: number, payload: Actividad) => api.put<Actividad>(`/api/actividades/${id}`, payload).then(res => res.data);
export const deleteActivity = (id: number) => api.delete(`/api/actividades/${id}`).then(res => res.data);
