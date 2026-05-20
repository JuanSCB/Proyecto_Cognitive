import { Link } from 'react-router-dom';

const NotFoundPage = () => (
  <div className="grid min-h-[60vh] place-items-center text-center">
    <div className="rounded-3xl border border-slate-200 bg-white p-14 shadow-soft">
      <p className="text-sm uppercase tracking-[0.24em] text-slate-500">404</p>
      <h1 className="mt-4 text-4xl font-semibold text-slate-900">Página no encontrada</h1>
      <p className="mt-3 text-slate-600">La ruta que buscas no existe o fue movida.</p>
      <Link to="/" className="mt-8 inline-flex rounded-3xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
        Volver al dashboard
      </Link>
    </div>
  </div>
);

export default NotFoundPage;
