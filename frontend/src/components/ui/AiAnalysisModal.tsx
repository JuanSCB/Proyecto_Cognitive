import React from 'react';
import Modal from './Modal';
import type { RoomAnalysisResponse } from '../../types/api';

interface Props {
  analysis: RoomAnalysisResponse | null;
  loading: boolean;
  onClose: () => void;
}

const AiAnalysisModal: React.FC<Props> = ({ analysis, loading, onClose }) => {
  if (!analysis && !loading) return null;

  return (
    <Modal title="Análisis Inteligente" onClose={onClose}>
      {loading ? (
        <div className="rounded-2xl bg-slate-50 p-4 text-sm text-slate-600">Generando diagnóstico con IA...</div>
      ) : analysis ? (
        <div className="space-y-4">
          <div className="grid gap-3 text-sm text-slate-700 sm:grid-cols-2">
            <div>
              <p className="font-semibold text-slate-500">Salón</p>
              <p className="mt-1 text-slate-900">{analysis.salon}</p>
            </div>
            <div>
              <p className="font-semibold text-slate-500">Fecha</p>
              <p className="mt-1 text-slate-900">{analysis.fecha}</p>
            </div>
            <div>
              <p className="font-semibold text-slate-500">Modelo utilizado</p>
              <p className="mt-1 text-slate-900">{analysis.modelo}</p>
            </div>
          </div>

          <div>
            <p className="mb-2 font-semibold text-slate-700">Diagnóstico generado por IA</p>
            <div className="max-h-64 overflow-y-auto rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm leading-7 text-slate-800 whitespace-pre-line">
              {analysis.analisis}
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={onClose}
              className="rounded-2xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700"
            >
              Cerrar
            </button>
          </div>
        </div>
      ) : null}
    </Modal>
  );
};

export default AiAnalysisModal;
