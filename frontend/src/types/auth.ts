export type AuthUser = {
  id: number;
  nombre: string;
  correo: string;
  rol: 'administrador' | 'alumno' | string;
};

export type AuthPayload = {
  token: string;
  usuario: AuthUser;
  message: string;
};
