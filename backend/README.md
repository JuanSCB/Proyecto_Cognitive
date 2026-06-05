# Sistema Inteligente de Iluminación

Backend REST construido con Python, Flask, SQLAlchemy y Flask-RESTX para monitorear y controlar un sistema inteligente de iluminación.

## Estructura del proyecto

- `app/`: aplicación Flask organizada en capas.
  - `controllers/`: endpoints REST.
  - `services/`: lógica de negocio.
  - `repositories/`: acceso a datos y consultas.
  - `models/`: modelos SQLAlchemy.
  - `routes/`: registro de namespaces.
  - `schemas/`: modelos Swagger/OpenAPI.
  - `config/`: configuración por ambiente.
  - `utils/`: helpers y manejo de errores.
- `migrations/`: scripts de migración de base de datos.
- `tests/`: pruebas unitarias.
- `.env`: variables de entorno.
- `bd.sql`: script para crear la base de datos MySQL.
- `run.py`: archivo de entrada para iniciar la API.
- `requirements.txt`: dependencias Python.

## Requisitos

- Python 3.11+ recomendado
- MySQL 5.7+ o MariaDB compatible
- Virtualenv

## Instalación

1. Crear el entorno virtual:
   ```bash
   python -m venv venv
   ```
2. Activar el entorno:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux / macOS:
     ```bash
     source venv/bin/activate
     ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de MySQL

1. Crear la base de datos y tablas con el script `bd.sql`:
   ```bash
   mysql -u <usuario> -p < bd.sql
   ```
2. Ajustar las variables en `.env`:
   ```text
   DB_USER=root
   DB_PASSWORD=strong_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=iluminacion_db
   ```

## Migraciones

Generar y aplicar migraciones:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

> Ya existe una migración inicial bajo `migrations/versions/0001_initial.py`.

## Ejecución

```bash
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

O directamente:

```bash
python run.py
```

## Documentación Swagger

La documentación Swagger está disponible en:

```
http://localhost:5000/docs
```

## Endpoints disponibles

- `GET /api/sensores`
- `POST /api/sensores`
- `GET /api/actividades`
- `POST /api/actividades`
- `PUT /api/actividades/<id>`
- `DELETE /api/actividades/<id>`
- `GET /api/configuracion`
- `PUT /api/configuracion`
- `GET /api/usuarios`
- `POST /api/usuarios`
- `GET /api/usuarios/<id>`
- `PUT /api/usuarios/<id>`
- `DELETE /api/usuarios/<id>`
- `GET /api/historial`
- `GET /api/consumo`
- `GET /api/salones`
- `GET /api/salones/<id>`
- `POST /api/salones`
- `PUT /api/salones/<id>`
- `DELETE /api/salones/<id>`
- `GET /api/salones/<id>/sensores`
- `GET /api/dashboard/salones`
- `GET /api/health`
- `GET /api/sensores/latest`
- `GET /api/reportes/promedio-lux`
- `GET /api/reportes/consumo-total`
- `GET /api/reportes/estadisticas`

### Payload de `POST /api/sensores`

```json
{
  "salon_id": 1,
  "lux": 320,
  "intensidad_led": 60,
  "consumo_energetico": 1.2,
  "modo_automatico": true,
  "actividad_id": 1
}
```

## Tests

```bash
pytest
```

## Notas

- El proyecto usa `Flask-RESTX` para documentación automática.
- `CORS` está habilitado para rutas `/api/*`.
- El backend está preparado para escalar con múltiples capas de negocio y repositorios.
