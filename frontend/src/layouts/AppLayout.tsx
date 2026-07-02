import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Header from '../components/ui/Header';
import { useAuth } from '../context/AuthContext';

const AppLayout = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const pages = [
    { name: 'Dashboard', path: '/' },
    { name: 'Salones', path: '/salones' },
    { name: 'Sensores', path: '/sensores' },
    { name: 'Historial', path: '/historial' },
    { name: 'Actividades', path: '/actividades' },
    { name: 'Reportes', path: '/reportes' },
    { name: 'Consumo', path: '/consumo' }
  ];

  if (user?.rol === 'administrador') {
    pages.push({ name: 'Configuración', path: '/configuracion' });
  }

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Header />
      <div className="mx-auto flex min-h-[calc(100vh-72px)] max-w-[1600px] gap-6 px-4 pb-10 pt-6 lg:px-8">
        <aside className="hidden w-72 flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-soft lg:flex">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Iluminación Inteligente</p>
            <h1 className="mt-3 text-2xl font-semibold text-slate-900">Panel de control</h1>
          </div>
          <nav className="mt-6 flex flex-col gap-1">
            {pages.map(page => (
              <NavLink
                key={page.path}
                to={page.path}
                end={page.path === '/'}
                className={({ isActive }) =>
                  `rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive ? 'bg-slate-900 text-white shadow-soft' : 'text-slate-700 hover:bg-slate-100'
                  }`
                }
              >
                {page.name}
              </NavLink>
            ))}
          </nav>

          <div className="mt-auto rounded-3xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm font-semibold text-slate-900">{user?.nombre ?? 'Usuario'}</p>
            <p className="text-sm text-slate-500 capitalize">{user?.rol ?? 'Invitado'}</p>
            <button
              type="button"
              onClick={() => {
                logout();
                navigate('/login');
              }}
              className="mt-4 w-full rounded-2xl bg-rose-600 px-4 py-3 text-sm font-semibold text-white hover:bg-rose-700"
            >
              Cerrar sesión
            </button>
          </div>
        </aside>

        <main className="w-full rounded-3xl bg-slate-50 p-0 shadow-none lg:flex-1 lg:bg-transparent">
          <div className="rounded-3xl bg-white p-6 shadow-soft">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
