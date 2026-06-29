import { useParams } from 'react-router-dom';
import useFetch from '../hooks/useFetch';
import api from '../api/axios';
import LoadingState from '../components/ui/LoadingState';
import Card from '../components/ui/Card';

const SalonHistoryPage = () => {
  const { id } = useParams();
  if (!id) return null;

  const sensoresState = useFetch(() => api.get(`/api/salones/${id}/sensores`).then(res => res.data), [id]);

  if (sensoresState.loading) return <LoadingState />;

  const sensores = Array.isArray(sensoresState.data) ? sensoresState.data : [];

  return (
    <div className="space-y-6">
      <Card title="Historial de lecturas">
        <div className="space-y-2">
          {sensores.length > 0 ? (
            sensores.map((s: any) => (
              <div key={s.id} className="rounded border border-slate-100 p-3">
                <p className="text-sm font-medium text-slate-900">Lectura #{s.id}</p>
                <div className="mt-2 grid gap-2 text-sm text-slate-600">
                  <p>Lux: {s.lux !== null && s.lux !== undefined ? Number(s.lux).toFixed(2) : '--'}</p>
                  <p>Intensidad LED: {s.intensidad_led !== null && s.intensidad_led !== undefined ? `${Number(s.intensidad_led).toFixed(0)}%` : '--'}</p>
                  <p>Consumo: {s.consumo_energetico !== null && s.consumo_energetico !== undefined ? `${Number(s.consumo_energetico).toFixed(2)} kWh` : '--'}</p>
                  <p>Modo: {s.modo_automatico === true ? 'Automático' : s.modo_automatico === false ? 'Manual' : '--'}</p>
                  <p className="text-xs text-slate-500">Registrado: {new Date(s.registrado_en).toLocaleString()}</p>
                </div>
              </div>
            ))
          ) : (
            <p className="text-sm text-slate-500">Sin registros disponibles.</p>
          )}
        </div>
      </Card>
    </div>
  );
};

export default SalonHistoryPage;
