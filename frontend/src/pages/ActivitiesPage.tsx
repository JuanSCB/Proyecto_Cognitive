import { FormEvent, useEffect, useMemo, useState } from 'react';
import Card from '../components/ui/Card';
import DataTable from '../components/ui/DataTable';
import LoadingState from '../components/ui/LoadingState';
import { useAuth } from '../context/AuthContext';
import { createActivity, deleteActivity, getActivities, updateActivity } from '../services/activitiesService';
import type { Actividad } from '../types/api';

const initialForm: Actividad = { nombre: '', descripcion: '' };

const ActivitiesPage = () => {
  const [activities, setActivities] = useState<Actividad[]>([]);
  const [form, setForm] = useState<Actividad>(initialForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const canEdit = user?.rol === 'profesor';

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
    if (!form.nombre.trim()) return;

    setLoading(true);
    try {
      if (editingId) {
        await updateActivity(editingId, form);
      } else {
        await createActivity(form);
      }
      setForm(initialForm);
      setEditingId(null);
      await refresh();
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
                    setForm({ nombre: activity.nombre, descripcion: activity.descripcion });
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
            <div className="flex items-end gap-3 sm:col-span-2">
              <button className="rounded-3xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
                {editingId ? 'Actualizar actividad' : 'Crear actividad'}
              </button>
              {editingId ? (
                <button
                  type="button"
                  onClick={() => {
                    setEditingId(null);
                    setForm(initialForm);
                  }}
                  className="rounded-3xl border border-slate-300 bg-white px-5 py-3 text-sm text-slate-700 hover:bg-slate-100"
                >
                  Cancelar
                </button>
              ) : null}
            </div>
          </form>
        ) : (
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-600">
            Solo los profesores pueden crear o editar actividades. Los alumnos pueden ver la lista.
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
