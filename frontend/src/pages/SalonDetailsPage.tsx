import { useParams } from 'react-router-dom';
import useFetch from '../hooks/useFetch';
import { getSalon } from '../services/dashboardService';
import api from '../api/axios';
import LoadingState from '../components/ui/LoadingState';
import Card from '../components/ui/Card';

const SalonDetailsPage = () => {
  const { id } = useParams();

  if (!id) return null;

  interface CumplimientoIluminacion {
    salon_id: number;
    porcentaje_adecuado: number;
    porcentaje_insuficiente: number;
    porcentaje_excesivo: number;
  }

  const salonState = useFetch(() => getSalon(id), [id]);
  const sensoresState = useFetch(() => api.get(`/api/salones/${id}/sensores`).then(res => res.data), [id]);
  const cumplimientoState = useFetch<CumplimientoIluminacion>(
    () => api.get(`/api/reportes/cumplimiento-iluminacion/${id}`).then(res => res.data),
    [id]
  );

  if (salonState.loading || sensoresState.loading) {
    return <LoadingState />;
  }

  // Diagnostic logs removed after switching to correct detail endpoint

  const salon = salonState.data ?? null;
  const sensores = Array.isArray(sensoresState.data) ? sensoresState.data : [];
  const hasSensores = sensores.length > 0;

  // Obtener el último registro (primero del array porque viene DESC)
  const ultimoRegistro = hasSensores ? sensores[0] : null;

  // Header datos
  const nombre = salon?.nombre ?? '';
  const ubicacion = salon?.ubicacion ?? '';
  const descripcion = salon?.descripcion ?? '';
  const actividadNombre = salon?.actividad_nombre ?? null;

  // Último registro: formatear datos
  const luxActual = ultimoRegistro?.lux !== null && ultimoRegistro?.lux !== undefined ? Number(ultimoRegistro.lux).toFixed(2) : '--';
  const intensidadLed = ultimoRegistro?.intensidad_led !== null && ultimoRegistro?.intensidad_led !== undefined ? `${Number(ultimoRegistro.intensidad_led).toFixed(0)}%` : '--';
  const consumoEnergy = ultimoRegistro?.consumo_energetico !== null && ultimoRegistro?.consumo_energetico !== undefined ? `${Number(ultimoRegistro.consumo_energetico).toFixed(2)} kWh` : '--';
  const modo = ultimoRegistro?.modo_automatico === true ? 'Automático' : ultimoRegistro?.modo_automatico === false ? 'Manual' : '--';
  const ultimaActualizacion = ultimoRegistro?.registrado_en ? new Date(ultimoRegistro.registrado_en).toLocaleString() : '--';

  return (
    <div className="space-y-6">
      {/* Encabezado con info del salón */}
      <div className="grid gap-2">
        <div>
          <h2 className="text-lg font-semibold">{nombre}</h2>
          <p className="text-sm text-slate-600">{ubicacion}</p>
          {descripcion && <p className="mt-1 text-sm text-slate-500">{descripcion}</p>}
          <p className="mt-3 text-sm text-slate-700">
            <span className="font-medium">🎯 Escenario actual:</span>{' '}
            {actividadNombre ?? 'Sin escenario asignado'}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <p className="text-sm text-slate-500">Estado:</p>
          <p className={`text-sm font-medium ${hasSensores ? 'text-emerald-600' : 'text-slate-500'}`}>
            {hasSensores ? 'En línea' : 'Sin datos'}
          </p>
        </div>
      </div>

      {actividadNombre ? (
        <Card title="Cumplimiento Histórico">
          {cumplimientoState.loading ? (
            <p className="text-sm text-slate-500">Cargando datos históricos...</p>
          ) : cumplimientoState.data &&
            typeof cumplimientoState.data.porcentaje_adecuado === 'number' &&
            typeof cumplimientoState.data.porcentaje_insuficiente === 'number' &&
            typeof cumplimientoState.data.porcentaje_excesivo === 'number' ? (
            <div className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl bg-emerald-50 p-4 text-sm text-slate-900">
                  <p className="font-semibold">🟢 Iluminación adecuada</p>
                  <p className="mt-3 text-2xl font-bold text-emerald-700">
                    {cumplimientoState.data.porcentaje_adecuado}%
                  </p>
                </div>
                <div className="rounded-2xl bg-yellow-50 p-4 text-sm text-slate-900">
                  <p className="font-semibold">🟡 Iluminación insuficiente</p>
                  <p className="mt-3 text-2xl font-bold text-amber-700">
                    {cumplimientoState.data.porcentaje_insuficiente}%
                  </p>
                </div>
                <div className="rounded-2xl bg-red-50 p-4 text-sm text-slate-900">
                  <p className="font-semibold">🔴 Iluminación excesiva</p>
                  <p className="mt-3 text-2xl font-bold text-red-700">
                    {cumplimientoState.data.porcentaje_excesivo}%
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm font-medium text-slate-900">
                    <span>Adecuada</span>
                    <span>{cumplimientoState.data.porcentaje_adecuado}%</span>
                  </div>
                  <div className="h-3 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className="h-full rounded-full bg-green-500"
                      style={{ width: `${cumplimientoState.data.porcentaje_adecuado}%` }}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm font-medium text-slate-900">
                    <span>Insuficiente</span>
                    <span>{cumplimientoState.data.porcentaje_insuficiente}%</span>
                  </div>
                  <div className="h-3 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className="h-full rounded-full bg-yellow-500"
                      style={{ width: `${cumplimientoState.data.porcentaje_insuficiente}%` }}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm font-medium text-slate-900">
                    <span>Excesiva</span>
                    <span>{cumplimientoState.data.porcentaje_excesivo}%</span>
                  </div>
                  <div className="h-3 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className="h-full rounded-full bg-red-500"
                      style={{ width: `${cumplimientoState.data.porcentaje_excesivo}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-500">No existen datos históricos suficientes para calcular el cumplimiento.</p>
          )}
        </Card>
      ) : (
        <Card title="Cumplimiento Histórico">
          <div className="space-y-2">
            <p className="text-sm text-slate-700">No existe un escenario asignado a este salón.</p>
            <p className="text-sm text-slate-500">Asigne un escenario de operación para poder evaluar el cumplimiento de iluminación.</p>
          </div>
        </Card>
      )}

      {!hasSensores ? (
        /* Sin sensores: mostrar tarjeta informativa */
        <Card title="No existen sensores asociados">
          <div className="space-y-2">
            <p className="text-sm text-slate-700">No existen sensores asociados a este salón.</p>
            <p className="text-sm text-slate-500">Este salón aún no tiene dispositivos ESP32 o sensores asociados.</p>
          </div>
        </Card>
      ) : (
        /* Con sensores: mostrar métricas y datos del último registro */
        <>
          {/* Tarjeta con métricas del último registro */}
          <Card title="Última lectura de sensores">
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Lux actual</p>
                  <p className="mt-2 text-2xl font-semibold text-slate-900">{luxActual}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Intensidad LED</p>
                  <p className="mt-2 text-2xl font-semibold text-slate-900">{intensidadLed}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Consumo energético</p>
                  <p className="mt-2 text-2xl font-semibold text-slate-900">{consumoEnergy}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Modo</p>
                  <p className="mt-2 text-2xl font-semibold text-slate-900">{modo}</p>
                </div>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-white p-4">
                <p className="text-xs text-slate-500">Última actualización</p>
                <p className="mt-2 text-sm font-medium text-slate-900">{ultimaActualizacion}</p>
              </div>
            </div>
          </Card>

          {/* Historial de sensores */}
          <Card title="Historial de sensores">
            <div className="space-y-2">
              {sensores.length > 0 ? (
                sensores.map((s: any) => (
                  <div key={s.id} className="rounded border border-slate-100 p-3">
                    <p className="text-sm font-medium text-slate-900">Sensor #{s.id}</p>
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
        </>
      )}
    </div>
  );
};

export default SalonDetailsPage;
