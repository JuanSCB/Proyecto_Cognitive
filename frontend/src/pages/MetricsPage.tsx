import { useEffect, useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import LineChart from '../components/ui/LineChart';
import LoadingState from '../components/ui/LoadingState';
import MetricTile from '../components/ui/MetricTile';
import useFetch from '../hooks/useFetch';
import { getSalones } from '../services/dashboardService';
import { getReport, getTotalConsumption, getStatistics, getAverageLux, getHistoryReport } from '../services/reportsService';
import type { DashboardSalon } from '../types/api';

const MetricsPage = () => {
  const [salones, setSalones] = useState<DashboardSalon[]>([]);
  const [selectedSalonId, setSelectedSalonId] = useState<number | undefined>(undefined);

  const reportState = useFetch(() => getReport(selectedSalonId), [selectedSalonId]);
  const totalConsumptionState = useFetch(() => getTotalConsumption(selectedSalonId), [selectedSalonId]);
  const statsState = useFetch(() => getStatistics(selectedSalonId), [selectedSalonId]);
  const averageLuxState = useFetch(() => getAverageLux(selectedSalonId), [selectedSalonId]);
  const historyState = useFetch(() => getHistoryReport(selectedSalonId), [selectedSalonId]);

  const values = useMemo(() => Array.isArray(historyState.data) ? historyState.data.map(record => record.lux) : [], [historyState.data]);
  const labels = useMemo(() => Array.isArray(historyState.data) ? historyState.data.map(record => new Date(record.registrado_en).toLocaleDateString()) : [], [historyState.data]);

  useEffect(() => {
    const loadSalones = async () => {
      try {
        setSalones(await getSalones());
      } catch {
        setSalones([]);
      }
    };
    loadSalones();
  }, []);

  if (reportState.loading || totalConsumptionState.loading || statsState.loading || averageLuxState.loading || historyState.loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h2 className="text-lg font-semibold">Reportes</h2>
          <p className="text-sm text-slate-500">Filtra el historial y métricas por salón.</p>
        </div>
        <div className="min-w-[240px]">
          <label className="mb-2 block text-sm font-semibold text-slate-700">Filtrar por salón</label>
          <select
            value={selectedSalonId ?? ''}
            onChange={event => setSelectedSalonId(event.target.value ? Number(event.target.value) : undefined)}
            className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-500"
          >
            <option value="">Todos los salones</option>
            {salones.map(salon => (
              <option key={salon.salon_id} value={salon.salon_id}>
                {salon.nombre}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricTile label="Energia total" value={`${totalConsumptionState.data?.total_consumo ?? 0} kWh`} />
        <MetricTile label="Promedio lux" value={`${averageLuxState.data?.promedio_lux?.toFixed(1) ?? 0}`} description="Promedio general" />
        <MetricTile label="Registros" value={reportState.data?.total_registros ?? 0} />
        <MetricTile label="Consumo histórico" value={`${statsState.data?.total_consumo_energetico?.toFixed(2) ?? 0} kWh`} />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card title="Gráfica histórica de lux">
          <LineChart points={values} labels={labels} />
        </Card>
        <Card title="Estadísticas del período">
          <div className="space-y-4 text-sm text-slate-600">
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="font-medium text-slate-900">Intensidad LED promedio</p>
              <p className="mt-2 text-3xl font-semibold">{statsState.data?.promedio_intensidad_led?.toFixed(1) ?? 0}%</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="font-medium text-slate-900">Cantidad de registros</p>
              <p className="mt-2 text-3xl font-semibold">{statsState.data?.cantidad_registros ?? 0}</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="font-medium text-slate-900">Último registro lux</p>
              <p className="mt-2 text-3xl font-semibold">{reportState.data?.ultimo_registro?.lux ?? '--'}</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default MetricsPage;
