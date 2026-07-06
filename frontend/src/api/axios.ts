import axios from 'axios';

const AUTH_STORAGE_KEY = 'iluminacion-auth';

const getStoredToken = () => {
  if (typeof window === 'undefined') return null;
  const stored = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!stored) return null;

  try {
    return JSON.parse(stored).token as string | null;
  } catch {
    return null;
  }
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? '/',
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(config => {
  const token = getStoredToken();
  if (token && config.headers) {
    const bearer = `Bearer ${token}`;
    // Asegurar ambas variantes de capitalización (algunos entornos/proxies
    // podrían normalizar a minúsculas). También añadimos una traza
    // ligera para poder comprobar desde la consola del navegador.
    config.headers.Authorization = bearer;
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    config.headers.authorization = bearer;

    if (import.meta.env.DEV) {
      // Mostrar en consola para diagnóstico local: método, url y si se añadió el header
      // No es información sensible en dev, evita imprimir el token en producción.
      // eslint-disable-next-line no-console
      console.debug('[api] attaching Authorization header', { method: config.method, url: config.url, hasAuth: Boolean(token) });
    }
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => Promise.reject(error?.response || error)
);

export default api;
