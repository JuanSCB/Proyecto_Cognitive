# Iluminación Inteligente - Frontend

Interfaz web para el sistema inteligente de iluminación, construida con React, Vite, Axios, React Router y TailwindCSS. La aplicación consume todos los endpoints definidos en `swagger.json` para monitoreo, gestión, reportes y configuración.

## Estructura

- `src/api` - configuración de Axios y cliente HTTP.
- `src/services` - servicios orientados a cada endpoint REST.
- `src/pages` - páginas principales del sistema.
- `src/components` - componentes UI reutilizables.
- `src/layouts` - estructura del dashboard y navegación.
- `src/hooks` - hooks personalizados para consumo de datos.
- `src/types` - tipos TypeScript generados para el API.

## Funcionalidades

- Dashboard principal con métricas clave.
- Monitoreo de sensores y últimos registros.
- Historial de lecturas con gráficas personalizadas.
- Gestión de actividades con creación, edición y eliminación.
- Visualización de métricas de consumo y reportes.
- Consumo energético con listado de registros.
- Configuración del sistema con ajuste de parámetros.

## Requisitos

- Node.js >= 18
- npm o Yarn

## Instalación

```bash
cd frontend
npm install
```

## Variables de entorno

La aplicación usa `VITE_API_BASE_URL` para apuntar al backend. Si no se configura, usará `/`.

Crea un archivo `.env` en la raíz del proyecto con:

```env
VITE_API_BASE_URL=http://localhost:5000
```

**Importante:** Asegúrate de que tu backend esté corriendo en la URL especificada. Si el backend corre en un puerto diferente, actualiza la variable de entorno correspondiente.

Ejemplo si el backend corre en puerto 3000:
```env
VITE_API_BASE_URL=http://localhost:3000
```

## Ejecución

```bash
npm run dev
```

Abrir `http://localhost:4173` en el navegador.

> Nota: el navegador puede mostrar "No es seguro" en local porque la aplicación se está sirviendo por HTTP y no por HTTPS. Esto es normal en desarrollo local. Para entorno de producción, debe usarse un servidor HTTPS con un certificado válido.

## Construcción

```bash
npm run build
```

## Buenas prácticas

- El código está organizado por dominios y responsabilidades.
- Se utiliza un hook reutilizable para fetch de datos.
- Los servicios consumen endpoints definidos en `swagger.json`.
- El diseño es responsive y escalable usando TailwindCSS.
