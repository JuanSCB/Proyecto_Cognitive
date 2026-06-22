# Arquitectura del Sistema de Roles

## Diagrama de Flujo de Autenticación

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                        │
└────────────────────────────────────┬──────────────────────────────┘
                                     │
                    ┌─────────────────┴────────────────────┐
                    │                                      │
            ┌───────▼────────┐                   ┌─────────▼──────┐
            │  Registro/Login│                   │  Hacer Request │
            │  (POST /auth)  │                   │  (GET /salones)│
            └───────┬────────┘                   └─────────┬──────┘
                    │                                      │
                    │ 1. Envía credenciales                │ 2. Envía token en
                    │ 2. Recibe token JWT                  │    header Authorization
                    │ 3. Guarda en localStorage            │
                    │                                      │
            ┌───────▼──────────────────────────────────────▼──────┐
            │                  BACKEND (Flask)                    │
            └────────────────────────┬─────────────────────────────┘
                                     │
                    ┌────────────────┴──────────────────┐
                    │                                   │
            ┌───────▼──────────────┐        ┌──────────▼────────┐
            │ /api/auth/login      │        │ Controlador Ruta  │
            │ /api/auth/register   │        │ (salon, activity) │
            └───────┬──────────────┘        └──────────┬────────┘
                    │                                  │
                    │ 1. Valida credenciales          │ 1. Extrae token del
                    │ 2. Hash de contraseña           │    header Authorization
                    │ 3. Crea JWT token               │ 2. Valida JWT
            ┌───────▼──────────────┐                   │ 3. Verifica rol
            │                      │        ┌──────────▼────────┐
            │ JWT Token:           │        │ Decorador         │
            │ {                    │        │ @require_role     │
            │   user_id: 1,        │        │ ('profesor')      │
            │   role: 'profesor',  │        └──────────┬────────┘
            │   exp: ...,          │                   │
            │   iat: ...           │                   │ ¿Es profesor?
            │ }                    │                   │
            └─────────────────────┘    ┌───────┬───────┴────┬─────────┐
                                       │       │            │         │
                                  ┌────▼──┐ ┌─▼────┐   ┌────▼──┐  ┌──▼────┐
                                  │ SÍ    │ │ NO   │   │ GET   │  │ POST/ │
                                  │Acceso │ │Error │   │ OK    │  │ PUT   │
                                  │Permite│ │403   │   │200    │  │ Error │
                                  └────────┘ └──────┘   └───────┘  └───────┘
                                                 
                    ┌────────────────────────────────────┐
                    │      BASE DE DATOS (MySQL)         │
                    │                                    │
                    │  tabla: usuarios                   │
                    │  ├─ id (int)                       │
                    │  ├─ nombre (varchar)               │
                    │  ├─ correo (varchar)               │
                    │  ├─ contraseña_hash (varchar)      │
                    │  ├─ rol (varchar)                  │
                    │  │   ├─ 'profesor'                 │
                    │  │   └─ 'alumno'                   │
                    │  └─ activo (boolean)               │
                    └────────────────────────────────────┘
```

## Matriz de Control de Acceso (RBAC)

```
╔═════════════════════════╦══════════╦═════════════╗
║ Endpoint                ║ Profesor ║ Alumno      ║
╠═════════════════════════╬══════════╬═════════════╣
║ GET /salones            ║ ✓        ║ ✓           ║
║ POST /salones           ║ ✓        ║ ✗ (403)     ║
║ PUT /salones/:id        ║ ✓        ║ ✗ (403)     ║
║ DELETE /salones/:id     ║ ✓        ║ ✗ (403)     ║
║                         ║          ║             ║
║ GET /actividades        ║ ✓        ║ ✓           ║
║ POST /actividades       ║ ✓        ║ ✗ (403)     ║
║ PUT /actividades/:id    ║ ✓        ║ ✗ (403)     ║
║ DELETE /actividades/:id ║ ✓        ║ ✗ (403)     ║
║                         ║          ║             ║
║ GET /sensores           ║ ✓        ║ ✓           ║
║ POST /sensores          ║ ✓        ║ ✗ (403)     ║
║                         ║          ║             ║
║ GET /configuracion      ║ ✓        ║ ✓           ║
║ PUT /configuracion      ║ ✓        ║ ✗ (403)     ║
║                         ║          ║             ║
║ GET /usuarios           ║ ✓        ║ ✗ (401)     ║
║ POST /usuarios          ║ ✓        ║ ✗ (401)     ║
║ PUT /usuarios/:id       ║ ✓        ║ ✗ (401)     ║
║ DELETE /usuarios/:id    ║ ✓        ║ ✗ (401)     ║
║                         ║          ║             ║
║ GET /historial          ║ ✓        ║ ✓           ║
║ GET /dashboard          ║ ✓        ║ ✓           ║
║ GET /reportes           ║ ✓        ║ ✓           ║
║                         ║          ║             ║
║ POST /auth/login        ║ ✓        ║ ✓           ║
║ POST /auth/register     ║ ✓        ║ ✓           ║
╚═════════════════════════╩══════════╩═════════════╝

✓ = Permitido
✗ = Denegado (con código de error)
  (401) = No autorizado (falta token)
  (403) = Prohibido (rol insuficiente)
```

## Flujo de Validación del Token

```
┌─────────────────────────────┐
│ Request HTTP               │
│ Headers:                    │
│ Authorization: Bearer <...> │
└────────────┬────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ ¿Existe header         │
    │ Authorization?         │
    └────┬──────────────┬────┘
         │              │
        NO             YES
         │              │
         ▼              ▼
    ┌─────────┐   ┌──────────────────────┐
    │Error 401│   │ Extrae token         │
    │Missing  │   │ (Bearer <token>)     │
    │Auth     │   └─────────┬────────────┘
    └─────────┘             │
                            ▼
                 ┌──────────────────────┐
                 │ Decodifica JWT       │
                 │ Verifica signature   │
                 └────┬─────────┬───────┘
                      │         │
                  Válido      Inválido
                      │         │
                      ▼         ▼
            ┌──────────────┐  ┌─────────────┐
            │ Extrae user_ │  │ Error 401   │
            │ id y role    │  │ Invalid     │
            │ de payload   │  │ Token       │
            └──────┬───────┘  └─────────────┘
                   │
                   ▼
        ┌────────────────────┐
        │ ¿Requiere rol      │
        │ específico?        │
        └────┬───────────┬───┘
             │           │
            NO         YES
             │           │
             ▼           ▼
        ┌────────┐  ┌──────────────┐
        │ Permite│  │ ¿Usuario con │
        │ acceso │  │ rol OK?      │
        │ 200    │  └────┬─────┬───┘
        └────────┘       │     │
                        SÍ    NO
                        │     │
                        ▼     ▼
                   ┌────────┐ ┌─────────┐
                   │Permite │ │Error 403│
                   │acceso  │ │Access   │
                   │200     │ │Denied   │
                   └────────┘ └─────────┘
```

## Componentes Principales

### 1. Modelo de Usuario (app/models/user.py)

```python
class Usuario:
    - id: int (PK)
    - nombre: str
    - correo: str (UNIQUE)
    - contraseña_hash: str (con salt)
    - rol: str ('profesor' | 'alumno')
    - activo: bool
    
    Methods:
    - set_password(contraseña): genera hash
    - check_password(contraseña): valida
    - es_profesor(): bool
    - es_alumno(): bool
```

### 2. Decorador de Autenticación (app/decorators.py)

```python
@require_role('profesor')
def endpoint_protegido():
    # Solo ejecuta si:
    # 1. Token JWT válido en Authorization header
    # 2. Usuario tiene rol 'profesor'
    # 3. Token no ha expirado
```

### 3. Controladores Protegidos

Patrón aplicado en todos los controladores:

```python
class SalonList(Resource):
    def get(self):
        # PÚBLICO - sin decorador
        return SalonService.list_salons()
    
    @require_role('profesor')  # ← Protegido
    def post(self, usuario_id, usuario_role):
        # Solo profesor puede crear
        return SalonService.create_salon(payload)
```

### 4. Flujo de Login/Registro

```
Frontend              Backend              Database
   │                   │                    │
   ├─ POST /login      │                    │
   ├──────────────────>│                    │
   │                   ├─ busca usuario    │
   │                   ├───────────────────>│
   │                   │<────────────────────┤
   │                   ├─ verifica pwd      │
   │                   ├─ crea JWT token    │
   │                   ├─ retorna token     │
   │<──────────────────┤                    │
   │ guarda token      │                    │
   │ en localStorage   │                    │
```

## Flujos de Solicitud Autenticada

### Flujo 1: Usuario Alumno consulta datos (GET)

```
1. Alumno hace login
   POST /auth/login {"correo": "alumno@...", "contraseña": "..."}
   → Recibe token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

2. Alumno solicita ver salones
   GET /salones
   Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   
3. Backend:
   ✓ Token válido
   ✓ Rol = 'alumno'
   ✓ GET no requiere rol específico
   → Retorna lista de salones (200)
```

### Flujo 2: Usuario Alumno intenta crear salón (POST)

```
1. Alumno intenta crear salón
   POST /salones
   Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Body: {"nombre": "Aula 101", ...}

2. Backend:
   @require_role('profesor') ← decorador
   ✓ Token válido
   ✗ Rol = 'alumno' (se requiere 'profesor')
   → Error 403: "Acceso denegado"
```

### Flujo 3: Usuario Profesor modifica datos (PUT)

```
1. Profesor solicita actualizar configuración
   PUT /configuracion
   Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Body: {"modo_automatico": true, ...}

2. Backend:
   @require_role('profesor') ← decorador
   ✓ Token válido
   ✓ Rol = 'profesor'
   ✓ PUT requiere rol 'profesor'
   → Actualiza y retorna datos (200)
```

## Seguridad

```
┌──────────────────────────────────────────┐
│ Medidas de Seguridad Implementadas       │
├──────────────────────────────────────────┤
│                                          │
│ 1. Contraseñas:                          │
│    ✓ Hash con werkzeug (scrypt)          │
│    ✓ Salt aleatorio incluido             │
│    ✓ Nunca se almacena plaintext         │
│                                          │
│ 2. Tokens JWT:                           │
│    ✓ Firmados con SECRET_KEY             │
│    ✓ Expiración: 24 horas                │
│    ✓ Verificación de signature           │
│    ✓ Validate timestamp (exp, iat)       │
│                                          │
│ 3. Autorización:                         │
│    ✓ Decorador en cada endpoint          │
│    ✓ Validación de rol antes de ejecutar │
│    ✓ No expone datos sensibles           │
│                                          │
│ 4. CORS:                                 │
│    ✓ Configurado para /api/*             │
│    ✓ Control de origins                  │
│                                          │
│ 5. HTTP Headers:                         │
│    ✓ Content-Type validation             │
│    ✓ Authorization header required       │
│                                          │
└──────────────────────────────────────────┘
```

## Códigos de Error HTTP

```
┌──────┬─────────────────────────────────────────┐
│ Code │ Descripción                             │
├──────┼─────────────────────────────────────────┤
│ 200  │ OK - Request exitoso                    │
│ 201  │ Created - Recurso creado                │
│ 400  │ Bad Request - Datos inválidos           │
│ 401  │ Unauthorized - Falta autenticación      │
│      │ - Falta token                          │
│      │ - Token inválido                       │
│      │ - Token expirado                       │
│ 403  │ Forbidden - Acceso denegado             │
│      │ - Rol insuficiente                     │
│ 404  │ Not Found - Recurso no existe           │
│ 500  │ Server Error - Error interno            │
└──────┴─────────────────────────────────────────┘
```

