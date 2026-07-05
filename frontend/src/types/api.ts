export interface SensorInput {
  lux: number;
  intensidad_led: number;
  consumo_energetico: number;
  modo_automatico: boolean;
  actividad_id?: number;
}

export interface Sensor {
  id: number;
  lux: number;
  intensidad_led: number;
  consumo_energetico: number;
  modo_automatico: boolean;
  actividad_id?: number;
  registrado_en: string;
}

export interface PaginatedSensores {
  items: Sensor[];
  page: number;
  limit: number;
  total: number;
}

export interface Actividad {
  id?: number;
  nombre: string;
  descripcion?: string;
}


export interface Usuario {
  id?: number;
  nombre: string;
  correo: string;
}

export interface ConsumoEnergetico {
  id: number;
  sensor_id: number;
  total_kwh: number;
  periodo_inicio: string;
  periodo_fin: string;
  creado_en: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
}

export interface Reporte {
  total_registros: number;
  energia_total: number;
  ultimo_registro: Sensor;
}

export interface PromedioLux {
  promedio_lux: number;
  cantidad_registros: number;
}

export interface ConsumoTotal {
  total_consumo: number;
}

export interface EstadisticasReportes {
  promedio_lux: number;
  promedio_intensidad_led: number;
  total_consumo_energetico: number;
  cantidad_registros: number;
  ultimo_registro: Sensor;
}

export interface Salon {
  id: number;
  nombre: string;
  ubicacion: string;
  descripcion?: string;
  creado_en?: string;
  actualizado_en?: string;
  actividad_id?: number | null;
  actividad_nombre?: string | null;
}

export interface DashboardSalon {
  salon_id: number;
  nombre: string;
  actividad_id?: number | null;
  actividad_nombre?: string | null;
  lux?: number | null;
  lux_minimo?: number | null;
  lux_maximo?: number | null;
  estado_iluminacion?: string | null;
  nivel_alerta?: string | null;
  intensidad_led?: number | null;
  consumo_energetico?: number | null;
  modo_automatico?: boolean | null;
}
