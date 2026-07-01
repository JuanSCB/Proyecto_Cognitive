import { FC, useState, type MouseEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeRoom } from '../../services/dashboardService';
import type { DashboardSalon, RoomAnalysisResponse } from '../../types/api';
import AiAnalysisModal from './AiAnalysisModal';

interface Props {
  salon: DashboardSalon;
}

const getAlertLevel = (nivel?: string | null, estado?: string | null) => {
  if (estado === 'Sin datos') {
    return {
      icon: '⚪',
      label: 'Sin monitoreo',
      badge: 'bg-slate-100 text-slate-700'
    };
  }

  switch (nivel) {
    case 'verde':
      return {
        icon: '🟢',
        label: 'Adecuada',
        badge: 'bg-green-100 text-green-700'
      };
    case 'amarillo':
      return {
        icon: '🟡',
        label: 'Cercana al límite',
        badge: 'bg-yellow-100 text-yellow-700'
      };
    case 'rojo':
      return {
        icon: '🔴',
        label: 'Fuera de rango',
        badge: 'bg-red-100 text-red-700'
      };
    default:
      return {
        icon: 'ℹ',
        label: 'Sin datos',
        badge: 'bg-slate-100 text-slate-700'
      };
  }
};

const SalonCard: FC<Props> = ({ salon }) => {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<RoomAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = () => {
    navigate(`/salones/${salon.salon_id}`);
  };

  const handleAnalyze = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation();
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const data = await analyzeRoom(salon.salon_id);
      setAnalysis(data);
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'data' in err && err.data && typeof err.data === 'object' && 'message' in err.data
        ? String(err.data.message)
        : 'No fue posible generar el análisis.';
      setError(message);
      window.alert(message);
    } finally {
      setLoading(false);
    }
  };

  const activityTitle = '🎯 Escenario de Operación';
  const activitySubtitle = salon.actividad_nombre
    ? salon.actividad_nombre
    : 'Sin escenario asignado';

  const alertStatus = getAlertLevel(salon.nivel_alerta ?? null, salon.estado_iluminacion ?? null);

  const luxDisplay = salon.lux !== null && salon.lux !== undefined
    ? Number(salon.lux).toFixed(2)
    : 'Sin datos';

  return (
    <div
      onClick={handleClick}
      className="cursor-pointer rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all hover:shadow-lg hover:border-slate-300 hover:-translate-y-1"
    >
      <div className="flex flex-col gap-3">
        <div>
          <h3 className="text-base font-semibold text-slate-900">{salon.nombre}</h3>
          <p className="mt-2 text-sm text-slate-500">{activityTitle}</p>
          <p className="text-sm font-semibold text-slate-900 truncate">{activitySubtitle}</p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-semibold ${alertStatus.badge}`}>
            {alertStatus.icon}
            {alertStatus.label}
          </span>
        </div>

        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Lux actual</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{luxDisplay}</p>
        </div>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={loading}
          className="rounded-2xl border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Analizando...' : 'Analizar con IA'}
        </button>
      </div>

      {error ? <p className="mt-3 text-sm text-rose-600">{error}</p> : null}
      <AiAnalysisModal analysis={analysis} loading={loading} onClose={() => setAnalysis(null)} />
    </div>
  );
};

export default SalonCard;
