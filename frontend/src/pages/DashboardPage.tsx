import { useMemo } from 'react';
import Card from '../components/ui/Card';
import LineChart from '../components/ui/LineChart';
import LoadingState from '../components/ui/LoadingState';
import MetricTile from '../components/ui/MetricTile';
import useFetch from '../hooks/useFetch';
import { getHealthStatus } from '../services/healthService';
import { getReport, getTotalConsumption, getStatistics, getAverageLux, getHistoryReport } from '../services/reportsService';

const DashboardPage = () => {
  const healthState = useFetch(getHealthStatus, []);
  const reportState = useFetch(getReport, []);
  const totalConsumptionState = useFetch(getTotalConsumption, []);
  const statsState = useFetch(getStatistics, []);
  const averageLuxState = useFetch(getAverageLux, []);
  const historyState = useFetch(getHistoryReport, []);

  const chartValues = useMemo(
    () =>
      Array.isArray(historyState.data)
        ? historyState.data.slice(-8).map(item => item.lux)
        : [],
    [historyState.data]
  );

  const chartLabels = useMemo(
    () =>
      Array.isArray(historyState.data)
        ? historyState.data.slice(-8).map(item => new Date(item.registrado_en).toLocaleDateString())
        : [],
    [historyState.data]
  );

  if (healthState.loading || reportState.loading || totalConsumptionState.loading || statsState.loading || averageLuxState.loading || historyState.loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricTile label="Estado del servicio" value={healthState.data?.status ?? 'Desconocido'} description={healthState.data?.service} />
        <MetricTile label="Registros totales" value={reportState.data?.total_registros ?? 0} description="Historial actualizado" />
        <MetricTile label="Consumo total" value={`${totalConsumptionState.data?.total_consumo ?? 0} kWh`} description="Consumo acumulado" />
        <MetricTile label="Lux promedio" value={`${averageLuxState.data?.promedio_lux?.toFixed(1) ?? 0}`} description={`${averageLuxState.data?.cantidad_registros ?? 0} registros`} />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <Card title="Visión general del sistema">
          <div className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm font-medium uppercase text-slate-500">Último registro</p>
                <p className="mt-3 text-2xl font-semibold text-slate-900">{reportState.data?.ultimo_registro?.lux ?? '--'}</p>
                <p className="mt-2 text-sm text-slate-500">Lux actual</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm font-medium uppercase text-slate-500">Promedio intensidad LED</p>
                <p className="mt-3 text-2xl font-semibold text-slate-900">{statsState.data?.promedio_intensidad_led?.toFixed(0) ?? '--'}%</p>
                <p className="mt-2 text-sm text-slate-500">Tendencia del historial</p>
              </div>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-soft">
              <h3 className="text-lg font-semibold text-slate-900">Últimas lecturas de lux</h3>
              <p className="mt-2 text-sm text-slate-500">Valores de los últimos registros disponibles para monitoreo.</p>
              <div className="mt-6">
                <LineChart points={chartValues} labels={chartLabels} />
              </div>
            </div>
          </div>
        </Card>

        <Card title="Resumen rápido">
          <div className="space-y-4">
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Registros por día</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{reportState.data?.total_registros ?? 0}</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Consumo promedio</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{((totalConsumptionState.data?.total_consumo ?? 0) / Math.max(reportState.data?.total_registros ?? 1, 1)).toFixed(2)} kWh</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Último registro</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{new Date(reportState.data?.ultimo_registro?.registrado_en ?? '').toLocaleString() || '--'}</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
