import api from '../api/axios';
import type { ConsumoEnergetico } from '../types/api';

export const getConsumptionList = (salonId?: number) =>
  api
    .get<ConsumoEnergetico[]>('/api/consumo', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);
