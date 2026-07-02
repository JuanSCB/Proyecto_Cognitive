import { FormEvent, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register as registerApi } from '../services/authService';

const RegisterPage = () => {
  const [nombre, setNombre] = useState('');
  const [correo, setCorreo] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [rol, setRol] = useState<'administrador' | 'alumno'>('alumno');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await registerApi({ nombre: nombre.trim(), correo: correo.trim(), contraseña, rol });
      navigate('/login');
    } catch (err: any) {
      setError(err?.data?.message ?? err?.message ?? 'Error al registrar usuario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-md items-center px-4 py-16">
      <div className="w-full rounded-3xl border border-slate-200 bg-white p-8 shadow-soft">
        <h1 className="text-2xl font-semibold text-slate-900">Registrar usuario</h1>
        <p className="mt-2 text-sm text-slate-600">Crea una cuenta de administrador o alumno para acceder al sistema.</p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <label className="block text-sm font-medium text-slate-700">
            Nombre completo
            <input
              type="text"
              value={nombre}
              onChange={event => setNombre(event.target.value)}
              required
              className="mt-2 w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
            />
          </label>

          <label className="block text-sm font-medium text-slate-700">
            Correo
            <input
              type="email"
              value={correo}
              onChange={event => setCorreo(event.target.value)}
              required
              className="mt-2 w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
            />
          </label>

          <label className="block text-sm font-medium text-slate-700">
            Contraseña
            <input
              type="password"
              value={contraseña}
              onChange={event => setContraseña(event.target.value)}
              required
              className="mt-2 w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
            />
          </label>

          <label className="block text-sm font-medium text-slate-700">
            Rol
            <select
              value={rol}
              onChange={event => setRol(event.target.value as 'administrador' | 'alumno')}
              className="mt-2 w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none focus:border-slate-500"
            >
              <option value="alumno">Alumno</option>
              <option value="administrador">Administrador</option>
            </select>
          </label>

          {error && <p className="text-sm text-rose-600">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-3xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {loading ? 'Registrando...' : 'Registrarme'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-500">
          ¿Ya tienes cuenta? <Link to="/login" className="font-semibold text-slate-900 underline">Inicia sesión</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
