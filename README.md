# Proyecto_Cognitive

Este repositorio contiene el frontend y backend del sistema inteligente de iluminación.

## Dockerización

Se agregaron los archivos necesarios para ejecutar la aplicación con Docker:

- `backend/Dockerfile`
- `backend/.dockerignore`
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `frontend/nginx.conf`
- `docker-compose.yml`

## Requisitos

- Docker instalado
- Docker Compose instalado

## Arrancar el proyecto con Docker

Desde la carpeta raíz `Proyecto_Cognitive`, ejecuta:

```bash
docker compose up --build
```

Esto iniciará los tres servicios:

- `db` (MySQL)
- `backend` (Flask)
- `frontend` (React + Nginx)

## URLs de acceso

- Frontend: `http://localhost:4173`
- Backend: `http://localhost:5000`

## Variables de entorno

El backend usa las variables definidas en `backend/.env` y el `docker-compose.yml` configura la conexión a MySQL.

El frontend se construye con `VITE_API_BASE_URL=http://localhost:5000`.

## Parar los contenedores

```bash
docker compose down
```

