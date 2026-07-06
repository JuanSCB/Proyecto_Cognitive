import { FormEvent, useEffect, useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import DataTable from '../components/ui/DataTable';
import LoadingState from '../components/ui/LoadingState';
import { useAuth } from '../context/AuthContext';
import { createActivity, deleteActivity, getActivities, updateActivity } from '../services/activitiesService';
import type { Actividad } from '../types/api';

type ActivityForm = Actividad & {
  lux_minimo: number | string;
  lux_maximo: number | string;
};

const initialForm: ActivityForm = { nombre: '', descripcion: '', lux_minimo: 100, lux_maximo: 6000 };

const ActivitiesPage = () => {
  const [activities, setActivities] = useState<Actividad[]>([]);
  const [form, setForm] = useState<ActivityForm>(initialForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [formError, setFormError] = useState<string | null>(null);
  const { user } = useAuth();
  const canEdit = user?.rol === 'administrador';

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        setActivities(await getActivities());
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const refresh = async () => {
    setLoading(true);
    try {
      setActivities(await getActivities());
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setFormError(null);

    if (!form.nombre.trim()) {
      setFormError('El nombre de la actividad es obligatorio.');
      return;
    }

    if (form.lux_minimo === '' || form.lux_maximo === '') {
      setFormError('Lux mínimo y Lux máximo son obligatorios.');
      return;
    }

    const lux_minimo = Number(form.lux_minimo);
    const lux_maximo = Number(form.lux_maximo);

    if (Number.isNaN(lux_minimo) || Number.isNaN(lux_maximo)) {
      setFormError('Lux mínimo y Lux máximo deben ser valores numéricos válidos.');
      return;
    }

    if (lux_minimo < 0) {
      setFormError('Lux mínimo debe ser mayor o igual a 0.');
      return;
    }

    if (lux_maximo <= lux_minimo) {
      setFormError('Lux máximo debe ser mayor que Lux mínimo.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...form,
        lux_minimo,
        lux_maximo,
      };

      if (editingId !== null) {
        await updateActivity(editingId, payload);
      } else {
        await createActivity(payload);
      }
      setForm(initialForm);
      setEditingId(null);
      setFormError(null);
      await refresh();
    } catch (error: any) {
      setFormError(error?.message ?? 'Error al guardar la actividad.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    setLoading(true);
    try {
      await deleteActivity(id);
      await refresh();
    } finally {
      setLoading(false);
    }
  };

  const rows = useMemo(
    () =>
      Array.isArray(activities) ? activities.map(activity => (
        <tr key={activity.id} className="border-t border-slate-200 even:bg-slate-50">
          <td className="px-4 py-3">{activity.id}</td>
          <td className="px-4 py-3">{activity.nombre}</td>
          <td className="px-4 py-3">{activity.descripcion || '-'}</td>
          <td className="px-4 py-3 space-x-2 text-sm text-slate-600">
            {canEdit ? (
              <>
                <button
                  type="button"
                  onClick={() => {
                    setEditingId(activity.id ?? null);
                    setForm({
                      nombre: activity.nombre,
                      descripcion: activity.descripcion,
                      lux_minimo: activity.lux_minimo ?? 100,
                      lux_maximo: activity.lux_maximo ?? 6000,
                    });
                  }}
                  className="rounded-2xl bg-slate-100 px-3 py-2 hover:bg-slate-200"
                >
                  Editar
                </button>
                <button
                  type="button"
                  onClick={() => activity.id && handleDelete(activity.id)}
                  className="rounded-2xl bg-rose-100 px-3 py-2 text-rose-700 hover:bg-rose-200"
                >
                  Eliminar
                </button>
              </>
            ) : (
              <span className="text-sm text-slate-500">Solo lectura</span>
            )}
          </td>
        </tr>
      )) : [],
    [activities, canEdit]
  );

  if (loading) {
    return <LoadingState />;
  }

  return (
    <div className="space-y-6">
      <Card title="Gestión de actividades">
        <p className="text-sm text-slate-500">Administra tareas y escenarios de iluminación.</p>
        {canEdit ? (
          <form onSubmit={handleSubmit} className="mt-6 grid gap-4 sm:grid-cols-2">
            <label className="space-y-2 text-sm text-slate-600">
              Nombre
              <input
                value={form.nombre}
                onChange={event => setForm(prev => ({ ...prev, nombre: event.target.value }))}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
                placeholder="Ej: Reunion nocturna"
                required
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Descripción
              <input
                value={form.descripcion}
                onChange={event => setForm(prev => ({ ...prev, descripcion: event.target.value }))}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
                placeholder="Detalle de la actividad"
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Lux mínimo
              <input
                type="number"
                min={0}
                step={1}
                value={form.lux_minimo}
                onChange={event => setForm(prev => ({ ...prev, lux_minimo: event.target.value === '' ? '' : Number(event.target.value) }))}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
                required
              />
            </label>
            <label className="space-y-2 text-sm text-slate-600">
              Lux máximo
              <input
                type="number"
                min={0}
                step={1}
                value={form.lux_maximo}
                onChange={event => setForm(prev => ({ ...prev, lux_maximo: event.target.value === '' ? '' : Number(event.target.value) }))}
                className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
                required
              />
            </label>
            <div className="flex flex-col gap-3 sm:col-span-2">
              {formError ? (
                <div className="rounded-3xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
                  {formError}
                </div>
              ) : null}
              <div className="flex items-end gap-3">
                <button className="rounded-3xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
                  {editingId ? 'Actualizar actividad' : 'Crear actividad'}
                </button>
                {editingId ? (
                  <button
                    type="button"
                    onClick={() => {
                      setEditingId(null);
                      setForm(initialForm);
                      setFormError(null);
                    }}
                    className="rounded-3xl border border-slate-300 bg-white px-5 py-3 text-sm text-slate-700 hover:bg-slate-100"
                  >
                    Cancelar
                  </button>
                ) : null}
              </div>
            </div>
          </form>
        ) : (
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-600">
            Solo los administradores pueden crear o editar actividades. Los alumnos pueden ver la lista.
          </div>
        )}
      </Card>

      <Card title="Lista de actividades">
        {activities.length ? (
          <DataTable
            headers={['ID', 'Nombre', 'Descripción', 'Acciones']}
            rows={rows}
          />
        ) : (
          <div className="rounded-3xl border border-dashed border-slate-200 p-8 text-center text-slate-500">
            No hay actividades registradas.
          </div>
        )}
      </Card>
    </div>
  );
};

export default ActivitiesPage;
