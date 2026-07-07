import React, { FC, useState } from 'react';
import type { Salon, Actividad } from '../../types/api';

interface Props {
  initial?: Partial<Salon>;
  activities?: Actividad[];
  onCancel: () => void;
  onSave: (payload: Partial<Salon>) => Promise<void> | void;
  requireActivitySelection?: boolean;
}

const SalonForm: FC<Props> = ({ initial = {}, activities = [], onCancel, onSave, requireActivitySelection = false }) => {
  const [nombre, setNombre] = useState(initial.nombre ?? '');
  const [ubicacion, setUbicacion] = useState(initial.ubicacion ?? '');
  const [descripcion, setDescripcion] = useState(initial.descripcion ?? '');
  const [actividadId, setActividadId] = useState<string>(
    initial.actividad_id !== undefined && initial.actividad_id !== null ? String(initial.actividad_id) : ''
  );
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!nombre.trim()) return setError('El nombre es obligatorio');
    if (!ubicacion.trim()) return setError('La ubicación es obligatoria');
    if (requireActivitySelection && actividadId === '') return setError('Debe seleccionar una actividad.');

    const payload: Partial<Salon> = {
      nombre: nombre.trim(),
      ubicacion: ubicacion.trim(),
      descripcion: descripcion.trim(),
      ...(actividadId !== '' ? { actividad_id: Number(actividadId) } : {})
    };

    await onSave(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p className="text-sm text-rose-600">{error}</p>}
      <div>
        <label className="text-sm text-slate-600">Nombre</label>
        <input
          value={nombre}
          onChange={e => setNombre(e.target.value)}
          className="mt-1 w-full rounded-md border px-3 py-2"
        />
      </div>
      <div>
        <label className="text-sm text-slate-600">Ubicación</label>
        <input
          value={ubicacion}
          onChange={e => setUbicacion(e.target.value)}
          className="mt-1 w-full rounded-md border px-3 py-2"
        />
      </div>
      <div>
        <label className="text-sm text-slate-600">Descripción</label>
        <textarea
          value={descripcion}
          onChange={e => setDescripcion(e.target.value)}
          className="mt-1 w-full rounded-md border px-3 py-2"
        />
      </div>
      <div>
        <label className="text-sm text-slate-600">Actividad Actual</label>
        <select
          value={actividadId}
          onChange={e => setActividadId(e.target.value)}
          className="mt-1 w-full rounded-md border px-3 py-2"
        >
          <option value="" disabled={requireActivitySelection}>
          {requireActivitySelection ? 'Seleccione una actividad' : 'Sin actividad'}
        </option>
          {activities.map(activity => (
            <option key={activity.id} value={activity.id}>
              {activity.nombre}
            </option>
          ))}
        </select>
      </div>

      <div className="flex justify-end gap-3">
        <button type="button" onClick={onCancel} className="rounded-md border px-4 py-2 text-sm">
          Cancelar
        </button>
        <button type="submit" className="rounded-md bg-slate-900 px-4 py-2 text-sm text-white">
          Guardar
        </button>
      </div>
    </form>
  );
};

export default SalonForm;
