import React, { FC } from 'react';

interface Props {
  title?: string;
  children: React.ReactNode;
  onClose: () => void;
}

const Modal: FC<Props> = ({ title, children, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-2xl rounded-2xl bg-white p-6">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <button className="text-slate-500" onClick={onClose}>Cerrar</button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

export default Modal;
