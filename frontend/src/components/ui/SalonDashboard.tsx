import React from 'react';
import useFetch from '../../hooks/useFetch';
import { getSalones } from '../../services/dashboardService';
import type { DashboardSalon } from '../../types/api';
import LoadingState from './LoadingState';
import SalonCard from './SalonCard';

const SalonDashboard: React.FC = () => {
  const state = useFetch(getSalones, []);

  if (state.loading) return <LoadingState />;

  const salones: DashboardSalon[] = Array.isArray(state.data) ? state.data : [];

  const total_salones = salones.length;
  const stats = salones.reduce(
    (acc, salon) => {
      if (salon.estado_iluminacion === 'Sin datos') {
        acc.sin_monitoreo += 1;
      } else if (salon.nivel_alerta === 'verde') {
        acc.adecuados += 1;
      } else if (salon.nivel_alerta === 'amarillo') {
        acc.cercanos_limite += 1;
      } else if (salon.nivel_alerta === 'rojo') {
        acc.fuera_rango += 1;
      }
      return acc;
    },
    {
      adecuados: 0,
      cercanos_limite: 0,
      fuera_rango: 0,
      sin_monitoreo: 0
    }
  );

  const { adecuados, cercanos_limite, fuera_rango, sin_monitoreo } = stats;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-500">Total salones</p>
          <p className="mt-3 text-3xl font-bold text-slate-900">{total_salones}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-500">🟢 Adecuados</p>
          <p className="mt-3 text-3xl font-bold text-emerald-700">{adecuados}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-500">🟡 Límite</p>
          <p className="mt-3 text-3xl font-bold text-amber-700">{cercanos_limite}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-500">🔴 Fuera de rango</p>
          <p className="mt-3 text-3xl font-bold text-red-700">{fuera_rango}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-500">⚪ Sin monitoreo</p>
          <p className="mt-3 text-3xl font-bold text-slate-700">{sin_monitoreo}</p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {salones.map((s: DashboardSalon) => (
          <SalonCard key={s.salon_id} salon={s} />
        ))}
      </div>
    </div>
  );
};

export default SalonDashboard;
