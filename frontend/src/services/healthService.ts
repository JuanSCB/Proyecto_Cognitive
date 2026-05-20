import api from '../api/axios';
import type { HealthStatus } from '../types/api';

export const getHealthStatus = () => api.get<HealthStatus>('/api/health').then(res => res.data);
