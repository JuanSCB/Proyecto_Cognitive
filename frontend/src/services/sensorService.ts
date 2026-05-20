import api from '../api/axios';
import type { PaginatedSensores, Sensor, SensorInput } from '../types/api';

export const getSensorList = (page = 1, limit = 20) =>
  api.get<PaginatedSensores>('/api/sensores', { params: { page, limit } }).then(res => res.data);
export const getSensorLatest = () => api.get<Sensor>('/api/sensores/latest').then(res => res.data);
export const createSensor = (payload: SensorInput) => api.post<Sensor>('/api/sensores', payload).then(res => res.data);
