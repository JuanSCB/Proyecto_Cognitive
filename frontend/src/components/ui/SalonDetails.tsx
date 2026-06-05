import React, { useMemo } from 'react';
import useFetch from '../../hooks/useFetch';
import { getSalon } from '../../services/dashboardService';
import LoadingState from './LoadingState';
import LineChart from './LineChart';
import Card from './Card';

interface Props {
  id: string;
}

const SalonDetails: React.FC<Props> = ({ id }) => {
  const state = useFetch(() => getSalon(id), [id]);

  const salon = state.data ?? {};

  const luxValues = useMemo(() => (Array.isArray((salon as any)?.historial_lux) ? (salon as any).historial_lux.map((p: any) => p.lux) : []), [salon]);
  const luxLabels = useMemo(() => (Array.isArray((salon as any)?.historial_lux) ? (salon as any).historial_lux.map((p: any) => new Date(p.registrado_en).toLocaleString()) : []), [salon]);

  const consumoValues = useMemo(() => (Array.isArray((salon as any)?.historial_consumo) ? (salon as any).historial_consumo.map((p: any) => p.consumo) : []), [salon]);
  const consumoLabels = useMemo(() => (Array.isArray((salon as any)?.historial_consumo) ? (salon as any).historial_consumo.map((p: any) => new Date(p.registrado_en).toLocaleString()) : []), [salon]);

  if (state.loading) return <LoadingState />;

  return (
    <div className="space-y-6">
      <Card title={`Salón: ${salon.nombre ?? id}`}>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <p className="text-sm text-slate-500">Lux actual</p>
            <p className="text-2xl font-semibold text-slate-900">{salon.lux_actual ?? '--'}</p>
          </div>
          <div>
            <p className="text-sm text-slate-500">Intensidad LED</p>
            <p className="text-2xl font-semibold text-slate-900">{salon.intensidad_led ?? '--'}%</p>
          </div>
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Historial de Lux">
          <LineChart points={luxValues} labels={luxLabels} />
        </Card>

        <Card title="Consumo energético">
          <LineChart points={consumoValues} labels={consumoLabels} />
        </Card>
      </div>

      <Card title="Historial de sensores">
        <div className="space-y-2">
          {Array.isArray(salon?.sensores) && salon.sensores.length > 0 ? (
            salon.sensores.map((s: any) => (
              <div key={s.id} className="rounded p-3 border border-slate-100">
                <p className="text-sm font-medium">{s.nombre}</p>
                <p className="text-sm text-slate-500">Lux: {s.lux}</p>
                <p className="text-sm text-slate-500">Registrado: {new Date(s.registrado_en).toLocaleString()}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-slate-500">Sin registros disponibles.</p>
          )}
        </div>
      </Card>

      <Card title="Actividad actual">
        {salon.actividad_actual ? (
          <div>
            <p className="text-sm font-medium">{salon.actividad_actual.nombre}</p>
            <p className="text-sm text-slate-500">Estado: {salon.actividad_actual.estado}</p>
          </div>
        ) : (
          <p className="text-sm text-slate-500">No hay actividad en este momento.</p>
        )}
      </Card>
    </div>
  );
};

export default SalonDetails;
