interface LineChartProps {
  points: number[];
  labels?: string[];
}

const LineChart = ({ points, labels }: LineChartProps) => {
  const max = Math.max(...points, 1);
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-4 shadow-soft">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-900">Historial</p>
        {labels?.length ? <span className="text-xs text-slate-500">{labels[0]} - {labels[labels.length - 1]}</span> : null}
      </div>
      <svg viewBox="0 0 240 100" className="h-40 w-full overflow-visible">
        <polyline
          fill="none"
          stroke="#2563eb"
          strokeWidth="3"
          points={points.map((value, index) => `${(240 / (points.length - 1 || 1)) * index},${100 - (value / max) * 92}`).join(' ')}
        />
        {points.map((value, index) => (
          <circle
            key={index}
            cx={(240 / (points.length - 1 || 1)) * index}
            cy={100 - (value / max) * 92}
            r="4"
            fill="#2563eb"
          />
        ))}
      </svg>
    </div>
  );
};

export default LineChart;
