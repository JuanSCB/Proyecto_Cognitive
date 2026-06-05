import React, { FC } from 'react';

interface Props {
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const ConfirmDialog: FC<Props> = ({ message, onConfirm, onCancel }) => {
  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-700">{message}</p>
      <div className="flex justify-end gap-3">
        <button onClick={onCancel} className="rounded-md border px-4 py-2 text-sm">Cancelar</button>
        <button onClick={onConfirm} className="rounded-md bg-rose-500 px-4 py-2 text-sm text-white">Eliminar</button>
      </div>
    </div>
  );
};

export default ConfirmDialog;
