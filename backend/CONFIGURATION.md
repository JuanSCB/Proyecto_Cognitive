Configuración del Sistema - Parámetros y uso

Este archivo documenta los parámetros expuestos en la entidad `Configuracion` y dónde se usan en el backend.

Parámetros (tabla `configuracion`):

- `modo_automatico` (boolean)
  - Descripción: Indica si el comportamiento por defecto del sistema es automático o manual.
  - Uso backend:
    - `SensorService.register_reading()` utiliza el valor del payload `modo_automatico` y muestra el modo actual en varios endpoints y respuestas del dashboard.
    - Se muestra en `ChatController` al describir el estado del salón.
  - Endpoints: GET/PUT `/api/configuracion` (controlador: `config_controller.py`)

- `intensidad_led_default` (integer)
  - Descripción: Valor por defecto de intensidad LED cuando el modo automático está activo y la iluminación ambiente está por debajo del umbral.
  - Uso backend:
    - `SensorService.register_reading()`: si `modo_automatico` está activado y `lux < umbral_lux`, se asigna `intensidad_led_default` al registro para mantener una intensidad por defecto.
  - Endpoints: GET/PUT `/api/configuracion`

- `umbral_lux` (integer)
  - Descripción: Umbral de luminosidad ambiental (lux) por debajo del cual, en modo automático, se fuerza la intensidad LED por defecto.
  - Uso backend:
    - `SensorService.register_reading()` compara `lux` con `config.umbral_lux` para decidir ajustes automáticos.
    - Se muestra como recomendación en `ChatController` y en la UI de configuración.
  - Endpoints: GET/PUT `/api/configuracion`

- `max_consumo` (float)
  - Descripción: Límite de consumo energético utilizado para métricas y alertas de consumo.
  - Uso backend:
    - Definido para reportes y posibles validaciones de consumo; aparece en modelos/Swagger y en la UI de configuración.
  - Endpoints: GET/PUT `/api/configuracion`

Notas adicionales:
- La sección `Configuración` está en uso activo por el backend y por varias vistas del frontend (SettingsPage, dashboard y Chatbot). Por tanto, la sección se conserva.
- Los endpoints y modelos Swagger relacionados están en `backend/app/controllers/config_controller.py` y `backend/app/schemas/swagger_models.py`.
- Si desea renombrar o reorganizar parámetros, actualice primero `ConfigRepository`/`ConfigService` y las migraciones correspondientes.

Archivos claves:
- `backend/app/models/configuracion.py`
- `backend/app/repositories/config_repository.py`
- `backend/app/services/config_service.py`
- `backend/app/controllers/config_controller.py`
- `frontend/src/pages/SettingsPage.tsx`
- `frontend/src/services/configService.ts`

Fin del documento.
