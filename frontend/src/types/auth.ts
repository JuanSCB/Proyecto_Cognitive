export type AuthUser = {
  id: number;
  nombre: string;
  correo: string;
  rol: 'profesor' | 'alumno' | string;
};

export type AuthPayload = {
  token: string;
  usuario: AuthUser;
  message: string;
};
