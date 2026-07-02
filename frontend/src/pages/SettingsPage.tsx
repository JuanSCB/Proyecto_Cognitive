import { FormEvent, useEffect, useState } from 'react';
import Card from '../components/ui/Card';
import LoadingState from '../components/ui/LoadingState';
import useFetch from '../hooks/useFetch';
import { useAuth } from '../context/AuthContext';
import { getConfiguration, updateConfiguration } from '../services/configService';
import type { Configuracion } from '../types/api';

const SettingsPage = () => {
  const { user } = useAuth();
  const canEdit = user?.rol === 'administrador';
  const configState = useFetch(getConfiguration, []);
  const [configuration, setConfiguration] = useState<Configuracion | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (configState.data) {
      setConfiguration(configState.data);
    }
  }, [configState.data]);

  if (!canEdit) {
    return (
      <div className="mx-auto flex min-h-screen items-center justify-center px-4 py-16">
        <div className="w-full max-w-xl rounded-3xl border border-slate-200 bg-white p-8 shadow-soft text-center">
          <h1 className="text-2xl font-semibold text-slate-900">Acceso denegado</h1>
          <p className="mt-4 text-sm text-slate-600">Solo los administradores pueden ver y editar la configuración del sistema.</p>
        </div>
      </div>
    );
  }

  if (configState.loading || !configuration) {
    return <LoadingState />;
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!configuration) return;
    setSaving(true);
    try {
      await updateConfiguration(configuration);
      alert('Configuración actualizada correctamente');
    } catch (error) {
      alert('No se pudo actualizar la configuración.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card title="Configuración del sistema">
        <p className="text-sm text-slate-500">Ajusta los valores de operación del sistema de iluminación.</p>
        {configuration ? (
          <form onSubmit={handleSubmit} className="mt-6 grid gap-6 sm:grid-cols-2">
            <label className="space-y-2 text-sm text-slate-600">
              Intensidad LED por defecto
              <input
                type="number"
                min={0}
                max={100}
                value={configuration.intensidad_led_default}
                onChange={event => setConfiguration({ ...configuration, intensidad_led_default: Number(event.target.value) })}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Umbral de lux
              <input
                type="number"
                min={0}
                value={configuration.umbral_lux}
                onChange={event => setConfiguration({ ...configuration, umbral_lux: Number(event.target.value) })}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Consumo máximo (kWh)
              <input
                type="number"
                step="0.01"
                min={0}
                value={configuration.max_consumo}
                onChange={event => setConfiguration({ ...configuration, max_consumo: Number(event.target.value) })}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
              />
            </label>
            <div className="space-y-2 text-sm text-slate-600">
              <span>Modo automático</span>
              <label className="inline-flex items-center gap-3 rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3">
                <input
                  type="checkbox"
                  checked={configuration.modo_automatico}
                  onChange={event => setConfiguration({ ...configuration, modo_automatico: event.target.checked })}
                  className="h-5 w-5 rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                />
                <span className="text-sm text-slate-700">Activado</span>
              </label>
            </div>
            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={saving}
                className="rounded-3xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {saving ? 'Guardando...' : 'Guardar configuración'}
              </button>
            </div>
          </form>
        ) : (
          <p className="text-sm text-slate-500">No se encontró configuración en la API.</p>
        )}
      </Card>
    </div>
  );
};

export default SettingsPage;
