import api from '../api/axios';
import type { ConsumoEnergetico } from '../types/api';

export const getConsumptionList = () => api.get<ConsumoEnergetico[]>('/api/consumo').then(res => res.data);
