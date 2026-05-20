import { useMemo } from 'react';
import Card from '../components/ui/Card';
import LineChart from '../components/ui/LineChart';
import LoadingState from '../components/ui/LoadingState';
import MetricTile from '../components/ui/MetricTile';
import useFetch from '../hooks/useFetch';
import { getReport, getTotalConsumption, getStatistics, getAverageLux, getHistoryReport } from '../services/reportsService';

const MetricsPage = () => {
  const reportState = useFetch(getReport, []);
  const totalConsumptionState = useFetch(getTotalConsumption, []);
  const statsState = useFetch(getStatistics, []);
  const averageLuxState = useFetch(getAverageLux, []);
  const historyState = useFetch(getHistoryReport, []);

  const values = useMemo(() => Array.isArray(historyState.data) ? historyState.data.map(record => record.lux) : [], [historyState.data]);
  const labels = useMemo(() => Array.isArray(historyState.data) ? historyState.data.map(record => new Date(record.registrado_en).toLocaleDateString()) : [], [historyState.data]);

  if (reportState.loading || totalConsumptionState.loading || statsState.loading || averageLuxState.loading || historyState.loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
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
