// Ejemplos de uso del sistema de roles desde el frontend (React)

// ============================================
// 1. SERVICIO DE AUTENTICACIÓN
// ============================================

// archivo: src/services/authService.ts

const API_BASE = 'http://localhost:5000/api';

interface Usuario {
  id: number;
  nombre: string;
  correo: string;
  rol: 'administrador' | 'alumno';
}

interface LoginResponse {
  token: string;
  usuario: Usuario;
  message: string;
}

export const authService = {
  // Login
  async login(correo: string, contraseña: string): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ correo, contraseña })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    const data = await response.json();
    // Guardar token en localStorage
    localStorage.setItem('token', data.token);
    localStorage.setItem('usuario', JSON.stringify(data.usuario));
    return data;
  },

  // Registro
  async register(
    nombre: string,
    correo: string,
    contraseña: string,
    rol: 'administrador' | 'alumno' = 'alumno'
  ): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, correo, contraseña, rol })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    const data = await response.json();
    localStorage.setItem('token', data.token);
    localStorage.setItem('usuario', JSON.stringify(data.usuario));
    return data;
  },

  // Logout
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
  },

  // Obtener usuario actual
  getUsuarioActual(): Usuario | null {
    const usuario = localStorage.getItem('usuario');
    return usuario ? JSON.parse(usuario) : null;
  },

  // Obtener token
  getToken(): string | null {
    return localStorage.getItem('token');
  },

  // Verificar si el usuario es administrador
  esAdministrador(): boolean {
    const usuario = this.getUsuarioActual();
    return usuario?.rol === 'administrador' ?? false;
  },

  // Verificar si el usuario es alumno
  esAlumno(): boolean {
    const usuario = this.getUsuarioActual();
    return usuario?.rol === 'alumno' ?? false;
  }
};

// ============================================
// 2. INTERCEPTOR AXIOS PARA INCLUIR TOKEN
// ============================================

// archivo: src/api/axios.ts

import axios from 'axios';
import { authService } from '../services/authService';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para agregar token a todas las requests
api.interceptors.request.use((config) => {
  const token = authService.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      authService.logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// ============================================
// 3. COMPONENTE DE LOGIN
// ============================================

// archivo: src/pages/LoginPage.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [correo, setCorreo] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setCargando(true);

    try {
      const resultado = await authService.login(correo, contraseña);
      
      // Redirigir según el rol
      if (resultado.usuario.rol === 'administrador') {
        navigate('/dashboard-administrador');
      } else {
        navigate('/dashboard-alumno');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al iniciar sesión');
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <h1>Iniciar Sesión</h1>
      {error && <div className="error">{error}</div>}
      
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Correo"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={contraseña}
          onChange={(e) => setContraseña(e.target.value)}
          required
        />
        <button type="submit" disabled={cargando}>
          {cargando ? 'Cargando...' : 'Iniciar Sesión'}
        </button>
      </form>

      <p>¿No tienes cuenta? <a href="/register">Regístrate aquí</a></p>
    </div>
  );
};

// ============================================
// 4. COMPONENTE PROTEGIDO POR ROL
// ============================================

// archivo: src/components/ProtectedRoute.tsx

import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'administrador' | 'alumno';
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requiredRole
}) => {
  const token = authService.getToken();
  const usuario = authService.getUsuarioActual();

  if (!token || !usuario) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && usuario.rol !== requiredRole) {
    return <Navigate to="/acceso-denegado" replace />;
  }

  return <>{children}</>;
};

// Uso en router:
// <Route
//   path="/crear-salon"
//   element={
//     <ProtectedRoute requiredRole="administrador">
//       <CrearSalonPage />
//     </ProtectedRoute>
//   }
// />

// ============================================
// 5. EJEMPLOS DE LLAMADAS A API
// ============================================

// archivo: src/services/salonService.ts

import api from '../api/axios';

export const salonService = {
  // Ver salones (todos)
  async obtenerSalones() {
    const response = await api.get('/salones');
    return response.data;
  },

  // Crear salón (solo administrador)
  async crearSalon(nombre: string, ubicacion: string, descripcion?: string) {
    const response = await api.post('/salones', {
      nombre,
      ubicacion,
      descripcion
    });
    return response.data;
  },

  // Actualizar salón (solo administrador)
  async actualizarSalon(id: number, datos: any) {
    const response = await api.put(`/salones/${id}`, datos);
    return response.data;
  },

  // Eliminar salón (solo administrador)
  async eliminarSalon(id: number) {
    const response = await api.delete(`/salones/${id}`);
    return response.data;
  }
};

// ============================================
// 6. COMPONENTE CON CONDICIONES POR ROL
// ============================================

// archivo: src/pages/SalonesPage.tsx

import React, { useEffect, useState } from 'react';
import { authService } from '../services/authService';
import { salonService } from '../services/salonService';

export const SalonesPage: React.FC = () => {
  const [salones, setSalones] = useState<any[]>([]);
  const esAdministrador = authService.esAdministrador();

  useEffect(() => {
    cargarSalones();
  }, []);

  const cargarSalones = async () => {
    try {
      const datos = await salonService.obtenerSalones();
      setSalones(datos);
    } catch (error) {
      console.error('Error al cargar salones:', error);
    }
  };

  const handleEliminar = async (id: number) => {
    if (!esAdministrador) {
      alert('Solo administradores pueden eliminar salones');
      return;
    }

    if (confirm('¿Estás seguro de que deseas eliminar este salón?')) {
      try {
        await salonService.eliminarSalon(id);
        cargarSalones();
      } catch (error) {
        alert('Error al eliminar salón');
      }
    }
  };

  return (
    <div className="salones-container">
      <h1>Salones</h1>

      {esAdministrador && (
        <button onClick={() => window.location.href = '/crear-salon'}>
          + Crear Nuevo Salón
        </button>
      )}

      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Ubicación</th>
            {esAdministrador && <th>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {salones.map((salon) => (
            <tr key={salon.id}>
              <td>{salon.nombre}</td>
              <td>{salon.ubicacion}</td>
              {esAdministrador && (
                <td>
                  <button onClick={() => window.location.href = `/editar-salon/${salon.id}`}>
                    Editar
                  </button>
                  <button onClick={() => handleEliminar(salon.id)} className="delete">
                    Eliminar
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// ============================================
// 7. HOOK PERSONALIZADO
// ============================================

// archivo: src/hooks/useAuth.ts

import { useEffect, useState } from 'react';
import { authService } from '../services/authService';

export const useAuth = () => {
  const [usuario, setUsuario] = useState(authService.getUsuarioActual());
  const [token, setToken] = useState(authService.getToken());

  const login = async (correo: string, contraseña: string) => {
    const resultado = await authService.login(correo, contraseña);
    setUsuario(resultado.usuario);
    setToken(authService.getToken());
    return resultado;
  };

  const logout = () => {
    authService.logout();
    setUsuario(null);
    setToken(null);
  };

  return {
    usuario,
    token,
    login,
    logout,
    esAdministrador: usuario?.rol === 'administrador',
    esAlumno: usuario?.rol === 'alumno',
    autenticado: !!token
  };
};

// Uso:
// const { usuario, login, logout, esAdministrador } = useAuth();
