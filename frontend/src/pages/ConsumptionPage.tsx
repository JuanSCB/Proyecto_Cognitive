import { useEffect, useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import DataTable from '../components/ui/DataTable';
import LoadingState from '../components/ui/LoadingState';
import MetricTile from '../components/ui/MetricTile';
import { getConsumptionList } from '../services/consumptionService';
import type { ConsumoEnergetico } from '../types/api';

const ConsumptionPage = () => {
  const [consumption, setConsumption] = useState<ConsumoEnergetico[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        setConsumption(await getConsumptionList());
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const totalEnergy = useMemo(() => Array.isArray(consumption) ? consumption.reduce((sum, item) => sum + item.total_kwh, 0) : 0, [consumption]);

  if (loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <MetricTile label="Consumo registrado" value={`${consumption.length ?? 0} entradas`} />
        <MetricTile label="Energía acumulada" value={`${totalEnergy.toFixed(2)} kWh`} />
        <MetricTile label="Periodo reciente" value={consumption[0]?.periodo_fin ? new Date(consumption[0].periodo_fin).toLocaleDateString() : '--'} />
      </div>

      <Card title="Consumo energético">
        {Array.isArray(consumption) && consumption.length ? (
          <DataTable
            headers={['ID', 'Sensor', 'Total (kWh)', 'Inicio', 'Fin', 'Creado']}
            rows={consumption.map(record => (
              <tr key={record.id} className="border-t border-slate-200 even:bg-slate-50">
                <td className="px-4 py-3">{record.id}</td>
                <td className="px-4 py-3">{record.sensor_id}</td>
                <td className="px-4 py-3">{record.total_kwh.toFixed(2)}</td>
                <td className="px-4 py-3">{new Date(record.periodo_inicio).toLocaleDateString()}</td>
                <td className="px-4 py-3">{new Date(record.periodo_fin).toLocaleDateString()}</td>
                <td className="px-4 py-3">{new Date(record.creado_en).toLocaleDateString()}</td>
              </tr>
            ))}
          />
        ) : (
          <div className="rounded-3xl border border-dashed border-slate-200 p-8 text-center text-slate-500">
            No se encontraron registros de consumo energético.
          </div>
        )}
      </Card>
    </div>
  );
};

export default ConsumptionPage;
