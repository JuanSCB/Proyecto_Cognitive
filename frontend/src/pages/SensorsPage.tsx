import { useEffect, useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import DataTable from '../components/ui/DataTable';
import LoadingState from '../components/ui/LoadingState';
import MetricTile from '../components/ui/MetricTile';
import { getSensorLatest, getSensorList } from '../services/sensorService';
import type { PaginatedSensores, Sensor } from '../types/api';

const SensorsPage = () => {
  const [page, setPage] = useState(1);
  const [sensors, setSensors] = useState<PaginatedSensores | null>(null);
  const [latest, setLatest] = useState<Sensor | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [sensorList, latestSensor] = await Promise.all([getSensorList(page, 10), getSensorLatest()]);
        setSensors(sensorList);
        setLatest(latestSensor);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [page]);

  const rows = useMemo(() => {
    return Array.isArray(sensors?.items) ? sensors.items.map(sensor => (
      <tr key={sensor.id} className="border-t border-slate-200 even:bg-slate-50">
        <td className="px-4 py-3">{sensor.id}</td>
        <td className="px-4 py-3">{sensor.lux}</td>
        <td className="px-4 py-3">{sensor.intensidad_led}%</td>
        <td className="px-4 py-3">{sensor.consumo_energetico.toFixed(2)} kWh</td>
        <td className="px-4 py-3">{sensor.modo_automatico ? 'Auto' : 'Manual'}</td>
        <td className="px-4 py-3">{new Date(sensor.registrado_en).toLocaleString()}</td>
      </tr>
    )) : [];
  }, [sensors]);

  if (loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 lg:grid-cols-3">
        <MetricTile label="Último sensor" value={latest?.lux ?? '--'} description="Lux más reciente" />
        <MetricTile label="Modo actual" value={latest?.modo_automatico ? 'Automático' : 'Manual'} />
        <MetricTile label="Consumo reciente" value={`${latest?.consumo_energetico?.toFixed(2) ?? '--'} kWh`} />
      </div>

      <Card title="Lista de sensores">
        {sensors?.items?.length ? (
          <DataTable
            headers={['ID', 'Lux', 'Intensidad LED', 'Consumo', 'Modo', 'Registrado']}
            rows={rows}
          />
        ) : (
          <div className="rounded-3xl border border-dashed border-slate-200 p-8 text-center text-slate-500">
            No hay registros de sensor disponibles.
          </div>
        )}

        <div className="mt-6 flex items-center justify-between text-sm text-slate-600">
          <p>
            Página {sensors?.page ?? 1} de {Math.ceil((sensors?.total ?? 1) / (sensors?.limit ?? 10))}
          </p>
          <div className="flex gap-3">
            <button
              disabled={!sensors || sensors.page <= 1}
              onClick={() => setPage(current => Math.max(1, current - 1))}
              className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700 transition hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Anterior
            </button>
            <button
              disabled={!sensors || sensors.page >= Math.ceil((sensors?.total ?? 0) / (sensors?.limit ?? 10))}
              onClick={() => setPage(current => current + 1)}
              className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700 transition hover:border-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Siguiente
            </button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default SensorsPage;
