import React, { useEffect, useState } from 'react';
import LoadingState from '../components/ui/LoadingState';
import Modal from '../components/ui/Modal';
import ConfirmDialog from '../components/ui/ConfirmDialog';
import SalonForm from '../components/ui/SalonForm';
import { getSalones, createSalon, updateSalon, deleteSalon } from '../services/salonesService';
import { getActivities } from '../services/activitiesService';
import type { Salon, Actividad } from '../types/api';

const SalonesPage = () => {
  const [salones, setSalones] = useState<Salon[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showCreate, setShowCreate] = useState(false);
  const [editing, setEditing] = useState<Salon | null>(null);
  const [deleting, setDeleting] = useState<Salon | null>(null);
  const [activities, setActivities] = useState<Actividad[]>([]);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getSalones();
      setSalones(Array.isArray(data) ? data : []);
    } catch (e: any) {
      setError(e?.message ?? 'Error al cargar salones');
    } finally {
      setLoading(false);
    }
  };

  const loadActivities = async () => {
    try {
      const data = await getActivities();
      setActivities(Array.isArray(data) ? data : []);
    } catch (e: any) {
      setError(e?.message ?? 'Error al cargar actividades');
    }
  };

  useEffect(() => {
    load();
    loadActivities();
  }, []);

  const handleCreate = async (payload: Partial<Salon>) => {
    try {
      await createSalon(payload);
      setShowCreate(false);
      await load();
    } catch (e: any) {
      setError(e?.message ?? 'Error al crear salón');
    }
  };

  const handleUpdate = async (payload: Partial<Salon>) => {
    if (!editing) return;
    try {
      await updateSalon(editing.id, payload);
      setEditing(null);
      await load();
    } catch (e: any) {
      setError(e?.message ?? 'Error al actualizar salón');
    }
  };

  const handleDelete = async () => {
    if (!deleting) return;
    try {
      await deleteSalon(deleting.id);
      setDeleting(null);
      await load();
    } catch (e: any) {
      setError(e?.message ?? 'Error al eliminar salón');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Salones</h2>
        <div>
          <button onClick={() => setShowCreate(true)} className="rounded-md bg-slate-900 px-4 py-2 text-sm text-white">Nuevo Salón</button>
        </div>
      </div>

      {loading ? (
        <LoadingState />
      ) : (
        <div className="rounded-2xl border border-slate-200 bg-white p-4">
          {error && <p className="mb-3 text-sm text-rose-600">{error}</p>}
          {salones.length === 0 ? (
            <p className="text-sm text-slate-500">No existen salones registrados.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full table-auto">
                <thead>
                  <tr className="text-left text-sm text-slate-600">
                    <th className="py-2">Nombre</th>
                    <th className="py-2">Ubicación</th>
                    <th className="py-2">Descripción</th>
                    <th className="py-2">Actividad Actual</th>
                    <th className="py-2">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {salones.map(s => (
                    <tr key={s.id} className="border-t">
                      <td className="py-3">
                        <div className="text-sm font-medium text-slate-900">{s.nombre}</div>
                      </td>
                      <td className="py-3 text-sm text-slate-700">{s.ubicacion}</td>
                      <td className="py-3 text-sm text-slate-700">{s.descripcion}</td>
                      <td className="py-3 text-sm text-slate-700">{s.actividad_nombre ?? 'Sin actividad'}</td>
                      <td className="py-3 text-sm text-slate-700">
                        <div className="flex gap-2">
                          <button onClick={() => setEditing(s)} className="rounded-md border px-3 py-1 text-sm">Editar</button>
                          <button onClick={() => setDeleting(s)} className="rounded-md border px-3 py-1 text-sm text-rose-600">Eliminar</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {showCreate && (
        <Modal title="Nuevo Salón" onClose={() => setShowCreate(false)}>
          <SalonForm activities={activities} onCancel={() => setShowCreate(false)} onSave={handleCreate} />
        </Modal>
      )}

      {editing && (
        <Modal title="Editar Salón" onClose={() => setEditing(null)}>
          <SalonForm initial={editing} activities={activities} onCancel={() => setEditing(null)} onSave={handleUpdate} />
        </Modal>
      )}

      {deleting && (
        <Modal title="Eliminar Salón" onClose={() => setDeleting(null)}>
          <ConfirmDialog message={`¿Desea eliminar este salón?`} onConfirm={handleDelete} onCancel={() => setDeleting(null)} />
        </Modal>
      )}
    </div>
  );
};

export default SalonesPage;
