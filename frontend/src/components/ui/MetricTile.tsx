interface MetricTileProps {
  label: string;
  value: string | number;
  accent?: string;
  description?: string;
}

const MetricTile = ({ label, value, accent = 'bg-cyan-500', description }: MetricTileProps) => (
  <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white via-slate-50 to-slate-100 p-5 shadow-soft">
    <span className="text-sm uppercase tracking-[0.22em] text-slate-500">{label}</span>
    <p className={`mt-3 text-3xl font-semibold text-slate-900 ${accent}`}>{value}</p>
    {description ? <p className="mt-2 text-sm text-slate-500">{description}</p> : null}
  </div>
);

export default MetricTile;
