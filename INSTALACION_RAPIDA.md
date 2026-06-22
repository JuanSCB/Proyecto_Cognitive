# Instalación Rápida - Sistema de Roles

## Resumen de Cambios Implementados

✅ **Modelo de Usuario Actualizado**
- Agregado campo `contraseña_hash`
- Agregado campo `activo`
- Rol por defecto: 'alumno'
- Métodos helper: `set_password()`, `check_password()`, `es_profesor()`, `es_alumno()`

✅ **Sistema de Autenticación JWT**
- Endpoints de login y registro
- Generación y validación de tokens JWT
- Tokens con expiración de 24 horas

✅ **Control de Acceso Basado en Roles (RBAC)**
- Decorador `@require_role('profesor')` para proteger endpoints
- Profesor: acceso completo (crear, modificar, eliminar)
- Alumno: acceso solo lectura

✅ **Endpoints Protegidos**
- POST/PUT/DELETE en: Salones, Actividades, Sensores, Configuración
- GET en Usuarios: solo profesor
- POST/PUT/DELETE en Usuarios: solo profesor

## Pasos de Instalación

### 1. Actualizar Base de Datos

```bash
# Opción A: Recargar el SQL completo
mysql -u root -p iluminacion_db < iluminacion_db.sql

# Opción B: Solo ejecutar el cambio (si ya existe la tabla)
mysql -u root -p iluminacion_db << EOF
ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) NOT NULL;
ALTER TABLE usuarios ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE usuarios MODIFY rol VARCHAR(50) NOT NULL DEFAULT 'alumno';
EOF
```

### 2. Insertar Usuarios de Prueba

```bash
mysql -u root -p iluminacion_db < usuarios_ejemplo.sql
```

Credenciales de prueba:
- **Profesor**: profesor@ejemplo.com / profesor123
- **Alumno**: alumno@ejemplo.com / alumno123

### 3. Instalar Dependencias

```bash
cd backend
pip install --upgrade -r requirements.txt
```

O solo la nueva dependencia:
```bash
pip install PyJWT>=2.8.0
```

### 4. Configurar Variable de Entorno (Opcional)

```bash
# En Linux/Mac
export SECRET_KEY="tu-clave-secreta-super-segura"

# En Windows PowerShell
$env:SECRET_KEY="tu-clave-secreta-super-segura"

# En Windows CMD
set SECRET_KEY=tu-clave-secreta-super-segura
```

### 5. Reiniciar el Servidor

```bash
cd backend
python run.py
```

## Probar la Implementación

### Via Swagger (Recomendado)

1. Abre http://localhost:5000/docs en tu navegador
2. Busca los endpoints `/api/auth/login` y `/api/auth/register`
3. Prueba hacer login con: profesor@ejemplo.com / profesor123
4. Copia el token de la respuesta
5. Click en "Authorize" (arriba a la derecha) e ingresa: `Bearer <token>`
6. Ahora puedes probar otros endpoints con protección

### Via curl

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}' \
  | jq -r '.token')

# 2. Ver salones (funciona con alumno también)
curl -X GET http://localhost:5000/api/salones \
  -H "Authorization: Bearer $TOKEN"

# 3. Crear salón (solo profesor)
curl -X POST http://localhost:5000/api/salones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nombre":"Aula 101","ubicacion":"Piso 2"}'
```

## Estructura de Archivos Nuevos/Modificados

```
backend/
├── app/
│   ├── decorators.py (NUEVO)
│   ├── controllers/
│   │   ├── auth_controller.py (NUEVO)
│   │   ├── salon_controller.py (MODIFICADO)
│   │   ├── activity_controller.py (MODIFICADO)
│   │   ├── sensor_controller.py (MODIFICADO)
│   │   ├── config_controller.py (MODIFICADO)
│   │   └── user_controller.py (MODIFICADO)
│   ├── models/
│   │   └── user.py (MODIFICADO)
│   ├── services/
│   │   └── user_service.py (MODIFICADO)
│   └── routes/
│       └── __init__.py (MODIFICADO)
├── requirements.txt (MODIFICADO - agregado PyJWT)
└── decorators.py (VIEJO - puede ser eliminado)

iluminacion_db.sql (MODIFICADO - tabla usuarios actualizada)
usuarios_ejemplo.sql (NUEVO)
SISTEMA_ROLES.md (NUEVO - documentación completa)
```

## Verificación

Para confirmar que todo funciona:

```bash
# 1. Verificar que el servidor inicia sin errores
python run.py

# 2. En otra terminal, probar login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}'

# 3. Debería retornar algo como:
# {
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "usuario": {...},
#   "message": "Bienvenido..."
# }
```

## Problemas Comunes

### Error: "No module named 'jwt'"
```bash
pip install PyJWT
```

### Error de BD: "Unknown column 'contraseña_hash'"
Asegúrate de haber ejecutado el SQL de actualización o recargar el dump completo.

### Token no funciona en Swagger
En Swagger, el formato debe ser: `Bearer <token>` (sin comillas, con el word "Bearer")

## Documentación

- [SISTEMA_ROLES.md](SISTEMA_ROLES.md) - Guía completa del sistema
- Swagger API: http://localhost:5000/docs

