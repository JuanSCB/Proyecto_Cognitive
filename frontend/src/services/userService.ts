import api from '../api/axios';
import type { Usuario } from '../types/api';

export const getUserList = () => api.get<Usuario[]>('/api/usuarios').then(res => res.data);
export const getUser = (id: number) => api.get<Usuario>(`/api/usuarios/${id}`).then(res => res.data);
export const createUser = (payload: Usuario) => api.post<Usuario>('/api/usuarios', payload).then(res => res.data);
export const updateUser = (id: number, payload: Usuario) => api.put<Usuario>(`/api/usuarios/${id}`, payload).then(res => res.data);
export const deleteUser = (id: number) => api.delete(`/api/usuarios/${id}`).then(res => res.data);
