import { useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import DataTable from '../components/ui/DataTable';
import LineChart from '../components/ui/LineChart';
import LoadingState from '../components/ui/LoadingState';
import useFetch from '../hooks/useFetch';
import { getHistory } from '../services/historyService';
import type { Sensor } from '../types/api';

const formatQuery = (date?: string) => (date ? date : undefined);

const HistoryPage = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const historyState = useFetch<Sensor[]>(() =>
    getHistory({ start_date: formatQuery(startDate), end_date: formatQuery(endDate) })
  , [startDate, endDate]);

  const chartData = useMemo(
    () =>
      Array.isArray(historyState.data)
        ? historyState.data.map(item => item.lux)
        : [],
    [historyState.data]
  );

  const chartLabels = useMemo(
    () =>
      Array.isArray(historyState.data)
        ? historyState.data.map(item => new Date(item.registrado_en).toLocaleDateString())
        : [],
    [historyState.data]
  );

  if (historyState.loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 lg:grid-cols-[1.5fr_1fr]">
        <Card title="Monitoreo de sensores">
          <p className="text-sm text-slate-500">Visualiza el comportamiento histórico de los sensores de iluminación.</p>
          <div className="mt-5 grid gap-4 sm:grid-cols-2">
            <label className="space-y-2 text-sm text-slate-600">
              Fecha inicio
              <input
                type="date"
                value={startDate}
                onChange={event => setStartDate(event.target.value)}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-500"
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Fecha fin
              <input
                type="date"
                value={endDate}
                onChange={event => setEndDate(event.target.value)}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-500"
              />
            </label>
          </div>
        </Card>
        <Card title="Resumen histórico">
          <div className="grid gap-4">
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Entradas</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{historyState.data?.length ?? 0}</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Lux máximo</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{Math.max(...(Array.isArray(historyState.data) ? historyState.data.map(item => item.lux) : [0])).toFixed(0)}</p>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Gráfica de historial de lux">
        <LineChart points={chartData} labels={chartLabels} />
      </Card>

      <Card title="Detalle de señales">
        {Array.isArray(historyState.data) && historyState.data.length ? (
          <DataTable
            headers={['ID', 'Lux', 'LED', 'Consumo', 'Modo', 'Registrado']}
            rows={historyState.data.map(sensor => (
              <tr key={sensor.id} className="border-t border-slate-200 even:bg-slate-50">
                <td className="px-4 py-3">{sensor.id}</td>
                <td className="px-4 py-3">{sensor.lux}</td>
                <td className="px-4 py-3">{sensor.intensidad_led}%</td>
                <td className="px-4 py-3">{sensor.consumo_energetico.toFixed(2)} kWh</td>
                <td className="px-4 py-3">{sensor.modo_automatico ? 'Auto' : 'Manual'}</td>
                <td className="px-4 py-3">{new Date(sensor.registrado_en).toLocaleString()}</td>
              </tr>
            ))}
          />
        ) : (
          <div className="rounded-3xl border border-dashed border-slate-200 p-8 text-center text-slate-500">
            No hay datos históricos para las fechas seleccionadas.
          </div>
        )}
      </Card>
    </div>
  );
};

export default HistoryPage;
