import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import type { DashboardSalon } from '../../types/api';

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

  const handleClick = () => {
    navigate(`/salones/${salon.salon_id}`);
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
      </div>
    </div>
  );
};

export default SalonCard;
