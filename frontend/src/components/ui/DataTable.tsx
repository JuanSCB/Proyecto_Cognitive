import { ReactNode } from 'react';

interface DataTableProps {
  headers: string[];
  rows: ReactNode | ReactNode[];
}

const DataTable = ({ headers, rows }: DataTableProps) => (
  <div className="overflow-x-auto rounded-3xl border border-slate-200 bg-slate-50 shadow-soft">
    <table className="min-w-full divide-y divide-slate-200 text-left text-sm text-slate-700">
      <thead className="bg-slate-100 text-slate-600">
        <tr>
          {headers.map(header => (
            <th key={header} className="px-4 py-3 font-semibold uppercase tracking-[0.12em]">
              {header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
);

export default DataTable;
