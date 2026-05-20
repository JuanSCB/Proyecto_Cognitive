import api from '../api/axios';
import type { Sensor } from '../types/api';

interface HistoryParams {
  start_date?: string;
  end_date?: string;
}

export const getHistory = ({ start_date, end_date }: HistoryParams = {}) =>
  api.get<Sensor[]>('/api/historial', { params: { start_date, end_date } }).then(res => res.data);
