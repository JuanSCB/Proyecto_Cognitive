import api from '../api/axios';
import type { Configuracion } from '../types/api';

export const getConfiguration = () => api.get<Configuracion>('/api/configuracion').then(res => res.data);
export const updateConfiguration = (payload: Configuracion) => api.put<Configuracion>('/api/configuracion', payload).then(res => res.data);
