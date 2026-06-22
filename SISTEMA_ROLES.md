# Sistema de Roles - Profesor y Alumno

## Descripción General

El sistema ahora soporta dos tipos de usuarios:

- **PROFESOR**: Acceso completo para crear, modificar y eliminar:
  - Salones
  - Actividades
  - Sensores
  - Configuración del sistema
  - Gestión de usuarios (crear, modificar, eliminar)

- **ALUMNO**: Acceso solo lectura (GET) para:
  - Ver salones
  - Ver actividades
  - Ver lecturas de sensores
  - Ver configuración
  - Ver historial
  - Ver reportes

## Tabla de Operaciones Permitidas

| Recurso | GET | POST | PUT | DELETE |
|---------|-----|------|-----|--------|
| Salones | Todos | Profesor | Profesor | Profesor |
| Actividades | Todos | Profesor | Profesor | Profesor |
| Sensores | Todos | Profesor | - | - |
| Configuración | Todos | - | Profesor | - |
| Usuarios | Profesor | Profesor | Profesor | Profesor |
| Historial | Todos | - | - | - |
| Reportes | Todos | - | - | - |
| Dashboard | Todos | - | - | - |

## Cambios en la Base de Datos

La tabla `usuarios` ahora incluye:

```sql
ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) NOT NULL;
ALTER TABLE usuarios ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE usuarios MODIFY rol VARCHAR(50) NOT NULL DEFAULT 'alumno';
```

## Cambios en el Modelo de Usuario

### Antes:
```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='usuario')
```

### Después:
```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='alumno')
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
    def set_password(self, contraseña):
        """Establece la contraseña con hash"""
        self.contraseña_hash = generate_password_hash(contraseña)
    
    def check_password(self, contraseña):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.contraseña_hash, contraseña)
    
    def es_profesor(self):
        """Verifica si el usuario es profesor"""
        return self.rol == 'profesor'
    
    def es_alumno(self):
        """Verifica si el usuario es alumno"""
        return self.rol == 'alumno'
```

## Nuevos Endpoints de Autenticación

### 1. Registro de Usuario

**POST** `/api/auth/register`

```json
{
  "nombre": "Juan Pérez",
  "correo": "juan@ejemplo.com",
  "contraseña": "micontraseña123",
  "rol": "alumno"  // o "profesor"
}
```

**Respuesta:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@ejemplo.com",
    "rol": "alumno"
  },
  "message": "Usuario Juan Pérez registrado exitosamente"
}
```

### 2. Login

**POST** `/api/auth/login`

```json
{
  "correo": "juan@ejemplo.com",
  "contraseña": "micontraseña123"
}
```

**Respuesta:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@ejemplo.com",
    "rol": "alumno"
  },
  "message": "Bienvenido Juan Pérez"
}
```

## Cómo Usar el Token JWT

Después de hacer login o registrarse, recibirás un token JWT. Para acceder a recursos protegidos, incluye el token en el header `Authorization`:

```
Authorization: Bearer <tu_token_jwt>
```

### Ejemplo con curl:

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}'

# Usar el token para crear un salón (solo profesor)
curl -X POST http://localhost:5000/api/salones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"nombre":"Aula 101","ubicacion":"Pabellon A"}'

# Ver salones (accesible para todos)
curl -X GET http://localhost:5000/api/salones \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Usuarios de Prueba

Se han creado usuarios de ejemplo en `usuarios_ejemplo.sql`:

| Correo | Contraseña | Rol |
|--------|-----------|-----|
| profesor@ejemplo.com | profesor123 | Profesor |
| alumno@ejemplo.com | alumno123 | Alumno |
| profesor2@ejemplo.com | profesor123 | Profesor |
| alumno2@ejemplo.com | alumno123 | Alumno |

Para insertar estos usuarios en la BD:

```bash
mysql -u root -p iluminacion_db < usuarios_ejemplo.sql
```

## Cambios de Dependencias

Se agregó PyJWT al `requirements.txt`:

```
PyJWT>=2.8.0
```

Instalar con:

```bash
pip install -r requirements.txt
```

## Errores Comunes

### 1. "No autorizado - Se requiere token de autenticación"

**Causa**: No enviaste el header `Authorization`

**Solución**: Incluye el token en el header:
```
Authorization: Bearer <token>
```

### 2. "Token expirado"

**Causa**: El token JWT expiró (por defecto 24 horas)

**Solución**: Haz login nuevamente para obtener un nuevo token

### 3. "Acceso denegado - Se requiere rol de profesor"

**Causa**: Intentaste acceder a un recurso restringido con una cuenta de alumno

**Solución**: Usa una cuenta de profesor o pide a un profesor que realice la operación

### 4. "Correo o contraseña inválidos"

**Causa**: Las credenciales no son correctas

**Solución**: Verifica que el correo y contraseña sean correctos

## Configuración

La clave secreta para firmar tokens se configura en `app/config/config.py`:

```python
SECRET_KEY = get_env('SECRET_KEY', 'change-me')
```

Por seguridad, cambia esta clave en producción usando una variable de entorno:

```bash
export SECRET_KEY="tu-clave-secreta-fuerte"
```

## Próximos Pasos

1. Actualiza la BD con el nuevo esquema
2. Carga los usuarios de ejemplo
3. Instala las dependencias nuevas: `pip install PyJWT`
4. Reinicia el servidor Flask
5. Prueba los endpoints de autenticación en Swagger en `/docs`

## Notas de Seguridad

- Las contraseñas se almacenan con hash (usando werkzeug.security)
- Los tokens JWT expiran después de 24 horas
- Siempre usa HTTPS en producción
- Mantén la `SECRET_KEY` segura y diferente en cada entorno
- Los alumnos no pueden ver ni modificar usuarios
- Los profesores tienen acceso completo a todos los recursos

