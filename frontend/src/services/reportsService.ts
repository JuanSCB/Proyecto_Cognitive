import api from '../api/axios';
import type { Reporte, ConsumoTotal, EstadisticasReportes, PromedioLux, Sensor } from '../types/api';

export const getReport = () => api.get<Reporte>('/api/reportes').then(res => res.data);
export const getTotalConsumption = () => api.get<ConsumoTotal>('/api/reportes/consumo-total').then(res => res.data);
export const getStatistics = () => api.get<EstadisticasReportes>('/api/reportes/estadisticas').then(res => res.data);
export const getHistoryReport = () => api.get<Sensor[]>('/api/reportes/historial').then(res => res.data);
export const getAverageLux = () => api.get<PromedioLux>('/api/reportes/promedio-lux').then(res => res.data);
