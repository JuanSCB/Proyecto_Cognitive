# Testing Rápido del Sistema de Roles

## ⚡ Quick Start Testing (5 minutos)

### 1. Preparación

```bash
# Terminal 1: Inicia el servidor
cd backend
python run.py

# Espera el mensaje: "Running on http://0.0.0.0:5000"
```

### 2. Testing en Swagger (Recomendado)

Abre en navegador: **http://localhost:5000/docs**

#### Test A: Registro de Usuario

1. Busca `POST /api/auth/register`
2. Click **"Try it out"**
3. Ingresa:
```json
{
  "nombre": "Test Usuario",
  "correo": "test@ejemplo.com",
  "contraseña": "test123456",
  "rol": "alumno"
}
```
4. Click **"Execute"**

✅ Esperado: Respuesta 201 Created

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 5,
    "nombre": "Test Usuario",
    "correo": "test@ejemplo.com",
    "rol": "alumno"
  },
  "message": "Usuario Test Usuario registrado exitosamente"
}
```

---

#### Test B: Login

1. Busca `POST /api/auth/login`
2. Click **"Try it out"**
3. Ingresa:
```json
{
  "correo": "profesor@ejemplo.com",
  "contraseña": "profesor123"
}
```
4. Click **"Execute"**

✅ Esperado: Respuesta 200 OK + token

---

#### Test C: Autorizar con Token

1. Click botón **"Authorize"** (arriba a la derecha)
2. En el campo, pega:
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
(Usa el token del Test B)

3. Click **"Authorize"**
4. Click **"Close"**

---

#### Test D: Ver Salones (GET - Para todos)

1. Busca `GET /api/salones`
2. Click **"Try it out"**
3. Click **"Execute"**

✅ Esperado: Respuesta 200 OK + lista salones

---

#### Test E: Crear Salón (POST - Solo Profesor)

1. Busca `POST /api/salones`
2. Click **"Try it out"**
3. Ingresa:
```json
{
  "nombre": "Aula de Testing",
  "ubicacion": "Piso 3",
  "descripcion": "Para pruebas del sistema"
}
```
4. Click **"Execute"**

✅ Esperado: Respuesta 201 Created

⚠️ Si obtienes 403: Verificar que el token sea de un profesor

---

#### Test F: Probar Restricción (Profesor vs Alumno)

1. Haz login como ALUMNO: `alumno@ejemplo.com` / `alumno123`
2. Copia el token y autorízate
3. Intenta `POST /api/salones`

❌ Esperado: Respuesta 403 Forbidden

```json
{
  "error": "Acceso denegado",
  "message": "Se requiere rol de profesor para esta operación"
}
```

---

### 3. Testing con curl (Terminal 2)

```bash
# Abre otra terminal (mantén server corriendo en Terminal 1)

# ===== 1. LOGIN =====
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}'

# Copia el token de la respuesta

# ===== 2. GUARDAR TOKEN EN VARIABLE =====
# Linux/Mac:
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}' \
  | grep -oP '"token":"\K[^"]*')

# Verificar:
echo $TOKEN

# ===== 3. GET SALONES (Sin protección) =====
curl -X GET http://localhost:5000/api/salones \
  -H "Authorization: Bearer $TOKEN"

# ===== 4. CREATE SALÓN (Protegido - Profesor) =====
curl -X POST http://localhost:5000/api/salones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nombre":"Aula de Testing",
    "ubicacion":"Piso 3",
    "descripcion":"Test desde curl"
  }'

# ===== 5. CREATE ACTIVIDAD (Protegido - Profesor) =====
curl -X POST http://localhost:5000/api/actividades \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "nombre":"Test Activity",
    "descripcion":"Descripción de prueba",
    "lux_minimo":300,
    "lux_maximo":500
  }'

# ===== 6. GET USUARIOS (Protegido - Profesor) =====
curl -X GET http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer $TOKEN"

# ===== 7. VERIFICAR ERROR 401 (Sin token) =====
curl -X GET http://localhost:5000/api/usuarios

# ===== 8. VERIFICAR ERROR 403 (Con token de alumno) =====
TOKEN_ALUMNO=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"alumno@ejemplo.com","contraseña":"alumno123"}' \
  | grep -oP '"token":"\K[^"]*')

curl -X POST http://localhost:5000/api/salones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN_ALUMNO" \
  -d '{"nombre":"Test","ubicacion":"Test"}'
```

---

## 📋 Test Cases Checklist

### Autenticación

- [ ] ✅ Registro con credenciales válidas → 201
- [ ] ✅ Registro con correo duplicado → 400
- [ ] ✅ Login con credenciales correctas → 200
- [ ] ✅ Login con credenciales incorrectas → 401
- [ ] ✅ Registro sin rol especificado → default 'alumno'

### Autorización

- [ ] ✅ Profesor puede crear salón → 201
- [ ] ✅ Alumno no puede crear salón → 403
- [ ] ✅ Profesor puede ver usuarios → 200
- [ ] ✅ Alumno no puede ver usuarios → 403
- [ ] ✅ Todos pueden ver salones → 200
- [ ] ✅ Todos pueden ver actividades → 200

### Token

- [ ] ✅ Request sin token → 401
- [ ] ✅ Token válido → permite acceso
- [ ] ✅ Token inválido → 401
- [ ] ✅ Token expirado → 401 (después de 24h)

### Validaciones

- [ ] ✅ Contraseña corta → error en registro
- [ ] ✅ Rol inválido → error en registro
- [ ] ✅ Correo vacío → error en registro

---

## 🔍 Verificación de Datos

### Verificar tabla usuarios en BD

```sql
mysql -u root -p iluminacion_db

-- Ver estructura
DESC usuarios;

-- Ver usuarios
SELECT id, nombre, correo, rol, activo FROM usuarios;

-- Ver estructura columna contraseña
SHOW COLUMNS FROM usuarios LIKE 'contraseña%';

-- Contar usuarios
SELECT COUNT(*) as total_usuarios FROM usuarios;

-- Contar por rol
SELECT rol, COUNT(*) FROM usuarios GROUP BY rol;
```

Esperado:
```
+----+--------+---------------------+-----------+--------+
| id | nombre | correo              | rol       | activo |
+----+--------+---------------------+-----------+--------+
|  1 | Juan   | profesor@ejemplo.com | profesor  |      1 |
|  2 | María  | alumno@ejemplo.com  | alumno    |      1 |
|  3 | Carlos | profesor2@...       | profesor  |      1 |
|  4 | Ana    | alumno2@...         | alumno    |      1 |
+----+--------+---------------------+-----------+--------+
```

---

## 🐛 Debugging - Si Algo Falla

### Error: "ModuleNotFoundError: No module named 'jwt'"

```bash
pip install PyJWT
# Verificar:
python -c "import jwt; print(jwt.__version__)"
```

### Error: "Unknown column 'contraseña_hash'"

```bash
# Recargar la BD
mysql -u root -p iluminacion_db < iluminacion_db.sql

# O manualmente:
mysql -u root -p iluminacion_db << EOF
ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) NOT NULL;
ALTER TABLE usuarios ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE usuarios MODIFY rol VARCHAR(50) NOT NULL DEFAULT 'alumno';
EOF
```

### Error: 404 "Not Found" en /api/auth/login

Verificar que:
1. Server está corriendo
2. Puerto es 5000
3. Ruta exacta es `/api/auth/login`
4. Método es POST

```bash
# Test rápido
curl -v http://localhost:5000/api/auth/login
```

### Error: Token no funciona en Swagger

1. Verificar formato: `Bearer <token>` (con espacio)
2. No agregar comillas
3. Copiar todo el token (no es muy largo)
4. No incluir caracteres adicionales

### Error: 401 "Unauthorized - Missing Auth"

Significado: Falta el header Authorization

Solución en Swagger:
1. Click "Authorize" (arriba a la derecha)
2. Ingresa: `Bearer <tu_token>`
3. Click "Authorize"

---

## 📊 Monitoreo

### Ver logs del servidor

Los logs mostrarán:
```
[INFO] GET /api/salones - 200 OK
[INFO] POST /api/salones - 201 Created (Profesor)
[WARNING] POST /api/salones - 403 Forbidden (Alumno)
[ERROR] POST /api/auth/login - 401 Unauthorized
```

### Ver requests en tiempo real

Con curl -v:
```bash
curl -v -X GET http://localhost:5000/api/salones \
  -H "Authorization: Bearer $TOKEN"
```

Mostrará headers request/response completos.

---

## ✅ Confirmación Final

Cuando todos los tests pasen:

```
✅ Autenticación funcionando
✅ Autorización funcionando
✅ Restricciones de rol implementadas
✅ BD actualizada correctamente
✅ Tokens JWT válidos
✅ Sistema listo para usar
```

---

## 📝 Notas

- Los tokens expiran después de 24 horas
- Las contraseñas se guardan hasheadas (no legibles)
- No se pueden ver las contraseñas reales en la BD
- Las respuestas 403 significan "usuario autenticado pero sin permisos"
- Las respuestas 401 significan "usuario no autenticado o token inválido"

---

**¡Sistema de roles completamente funcional! 🎉**
