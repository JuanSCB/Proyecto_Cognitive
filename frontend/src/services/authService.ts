import api from '../api/axios';

type LoginPayload = {
  correo: string;
  contraseña: string;
};

export type AuthUser = {
  id: number;
  nombre: string;
  correo: string;
  rol: 'administrador' | 'alumno' | string;
};

export type LoginResponse = {
  token: string;
  usuario: AuthUser;
  message: string;
};

export const login = (payload: LoginPayload) =>
  api.post<LoginResponse>('/api/auth/login', payload).then(res => res.data);

export const register = (payload: LoginPayload & { nombre: string; rol?: string }) =>
  api.post<LoginResponse>('/api/auth/register', payload).then(res => res.data);
