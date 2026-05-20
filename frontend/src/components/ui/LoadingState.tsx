const LoadingState = () => (
  <div className="flex min-h-[220px] items-center justify-center rounded-3xl border border-dashed border-slate-300 bg-slate-50">
    <div className="flex items-center gap-3 text-slate-600">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-300 border-t-slate-900"></div>
      <span>Cargando datos...</span>
    </div>
  </div>
);

export default LoadingState;
