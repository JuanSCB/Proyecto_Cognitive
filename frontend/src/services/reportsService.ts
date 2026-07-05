import api from '../api/axios';
import type { Reporte, ConsumoTotal, EstadisticasReportes, PromedioLux, Sensor } from '../types/api';

export const getReport = (salonId?: number) =>
  api
    .get<Reporte>('/api/reportes', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);

export const getTotalConsumption = (salonId?: number) =>
  api
    .get<ConsumoTotal>('/api/reportes/consumo-total', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);

export const getStatistics = (salonId?: number) =>
  api
    .get<EstadisticasReportes>('/api/reportes/estadisticas', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);

export const getHistoryReport = (salonId?: number) =>
  api
    .get<Sensor[]>('/api/reportes/historial', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);

export const getAverageLux = (salonId?: number) =>
  api
    .get<PromedioLux>('/api/reportes/promedio-lux', {
      params: salonId ? { salon_id: salonId } : {}
    })
    .then(res => res.data);
