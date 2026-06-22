# Checklist de Implementación - Sistema de Roles

## Pre-Requisitos ✓

- [ ] Base de datos MySQL funcionando
- [ ] Servidor Flask instalado (`pip install Flask`)
- [ ] Git clonado o archivos descargados
- [ ] Acceso a línea de comandos/terminal

## Paso 1: Actualizar Base de Datos

### Opción A: Recargar dump completo (Recomendado si es nueva instalación)

```bash
mysql -u root -p iluminacion_db < iluminacion_db.sql
```

Checklist:
- [ ] Base de datos `iluminacion_db` existe
- [ ] Usuario root o equivalente configurado
- [ ] Archivo `iluminacion_db.sql` actualizado (con los cambios de usuarios)
- [ ] Comando ejecutado sin errores
- [ ] Verificar tabla usuarios: `DESC usuarios;`

### Opción B: Actualizar tabla existente (Si ya tiene datos importantes)

```bash
mysql -u root -p iluminacion_db << EOF
ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) NOT NULL;
ALTER TABLE usuarios ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE usuarios MODIFY rol VARCHAR(50) NOT NULL DEFAULT 'alumno';
EOF
```

Checklist:
- [ ] Copias de seguridad realizadas
- [ ] Alter Table ejecutado sin errores
- [ ] Estructura verificada: `DESC usuarios;`

## Paso 2: Cargar Usuarios de Ejemplo

```bash
mysql -u root -p iluminacion_db < usuarios_ejemplo.sql
```

Checklist:
- [ ] Archivo `usuarios_ejemplo.sql` existe
- [ ] Comando ejecutado sin errores
- [ ] Verificar usuarios: `SELECT id, nombre, correo, rol FROM usuarios;`

Deberías ver 4 usuarios:
- profesor@ejemplo.com (Profesor)
- alumno@ejemplo.com (Alumno)
- profesor2@ejemplo.com (Profesor)
- alumno2@ejemplo.com (Alumno)

## Paso 3: Actualizar Dependencias

```bash
cd backend
pip install --upgrade -r requirements.txt
```

O solo PyJWT:
```bash
pip install PyJWT>=2.8.0
```

Checklist:
- [ ] Navegar a carpeta backend
- [ ] Comando ejecutado sin errores
- [ ] Verificar instalación: `pip show PyJWT`

## Paso 4: Verificar Archivos Modificados

```bash
backend/
├── app/
│   ├── decorators.py (NUEVO)
│   ├── models/
│   │   └── user.py (MODIFICADO)
│   ├── controllers/
│   │   ├── auth_controller.py (NUEVO)
│   │   ├── salon_controller.py (MODIFICADO)
│   │   ├── activity_controller.py (MODIFICADO)
│   │   ├── sensor_controller.py (MODIFICADO)
│   │   ├── config_controller.py (MODIFICADO)
│   │   └── user_controller.py (MODIFICADO)
│   ├── services/
│   │   └── user_service.py (MODIFICADO)
│   └── routes/
│       └── __init__.py (MODIFICADO)
└── requirements.txt (MODIFICADO)
```

Checklist:
- [ ] Archivo `app/decorators.py` existe
- [ ] Archivo `app/controllers/auth_controller.py` existe
- [ ] Archivo `backend/decorators.py` puede ser eliminado (viejo)
- [ ] requirements.txt incluye PyJWT>=2.8.0

## Paso 5: Configurar Variable de Entorno (Opcional pero Recomendado)

### Linux/Mac:
```bash
export SECRET_KEY="mi-clave-secreta-super-segura-123"
export DEBUG="False"
```

### Windows PowerShell:
```powershell
$env:SECRET_KEY="mi-clave-secreta-super-segura-123"
$env:DEBUG="False"
```

### Windows CMD:
```cmd
set SECRET_KEY=mi-clave-secreta-super-segura-123
set DEBUG=False
```

### .env file (Alternativa):
Crear archivo `backend/.env`:
```
SECRET_KEY=mi-clave-secreta-super-segura-123
DEBUG=False
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=iluminacion_db
```

Checklist:
- [ ] Variable SECRET_KEY configurada
- [ ] Para producción: usar clave fuerte (mínimo 32 caracteres)
- [ ] Nunca commitear claves en git

## Paso 6: Iniciar Servidor

```bash
cd backend
python run.py
```

Checklist:
- [ ] Server inicia sin errores
- [ ] Mensaje: "Running on http://0.0.0.0:5000"
- [ ] No hay ImportError de decorators
- [ ] No hay ImportError de PyJWT

## Paso 7: Verificación Inicial

### 7.1: Abrir Swagger

Abrir en navegador: http://localhost:5000/docs

Checklist:
- [ ] Swagger carga correctamente
- [ ] Endpoints `/api/auth/login` y `/api/auth/register` visibles
- [ ] Endpoints protegidos tienen candado 🔒

### 7.2: Probar Login

En Swagger:
1. Click en `/api/auth/login` → "Try it out"
2. Ingresar:
   ```json
   {
     "correo": "profesor@ejemplo.com",
     "contraseña": "profesor123"
   }
   ```
3. Click "Execute"

Checklist:
- [ ] Respuesta 200 OK
- [ ] Token recibido
- [ ] Usuario info completo
- [ ] Rol = "profesor"

### 7.3: Probar Endpoint Protegido

En Swagger:
1. Click en botón "Authorize" (arriba a la derecha)
2. Copiar el token de la respuesta anterior
3. Ingresar: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
4. Click "Authorize"
5. Probar GET `/api/salones` → "Try it out" → "Execute"

Checklist:
- [ ] Respuesta 200 OK
- [ ] Se obtiene lista de salones
- [ ] Autenticación funciona

### 7.4: Probar Restricción de Rol

En Swagger (mismo token):
1. Ir a POST `/api/salones`
2. Click "Try it out"
3. Ingresar datos del nuevo salón
4. Click "Execute"

Checklist:
- [ ] Respuesta 201 Created (si es profesor)
- [ ] O Respuesta 403 Forbidden (si intentas con alumno)

### 7.5: Test con Alumno

Repetir login con:
```json
{
  "correo": "alumno@ejemplo.com",
  "contraseña": "alumno123"
}
```

Checklist:
- [ ] Login exitoso
- [ ] GET `/api/salones` funciona (200)
- [ ] POST `/api/salones` retorna 403
- [ ] GET `/api/usuarios` retorna 401

## Paso 8: Pruebas con curl

```bash
# 1. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}'

# 2. Guardar token en variable (Linux/Mac)
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}' \
  | grep -oP '"token":"\K[^"]*')

# 3. Usar token para GET
curl -X GET http://localhost:5000/api/salones \
  -H "Authorization: Bearer $TOKEN"

# 4. Usar token para POST
curl -X POST http://localhost:5000/api/salones \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nombre":"Aula 101","ubicacion":"Piso 2"}'
```

Checklist:
- [ ] Todos los comandos ejecutados sin errores
- [ ] Respuestas esperadas recibidas
- [ ] Token funciona correctamente

## Paso 9: Integración Frontend (Opcional)

Si usas React:

1. [ ] Copiar código de `EJEMPLOS_INTEGRACION.ts`
2. [ ] Crear servicio de autenticación
3. [ ] Crear componente de login
4. [ ] Crear componente protegido por rol
5. [ ] Integrar en rutas de aplicación

Ver archivo: `frontend/EJEMPLOS_INTEGRACION.ts`

## Paso 10: Seguridad - Revisión Final

Checklist de seguridad:

- [ ] SECRET_KEY no es el valor por defecto
- [ ] Contraseñas de BD no están en código
- [ ] .env no está en git (agregar a .gitignore)
- [ ] CORS configurado apropiadamente
- [ ] Usar HTTPS en producción
- [ ] Cambiar contraseñas de usuarios de ejemplo en producción
- [ ] Verificar permisos de archivos

## Paso 11: Documentación

- [ ] Leer `SISTEMA_ROLES.md` completo
- [ ] Leer `ARQUITECTURA_ROLES.md` para entender flujos
- [ ] Guardar `INSTALACION_RAPIDA.md` como referencia

## Troubleshooting

### Error: "No module named 'jwt'"

```bash
pip install PyJWT
```

### Error: "Unknown column 'contraseña_hash'"

Asegúrate de ejecutar el SQL:
```bash
mysql -u root -p iluminacion_db < iluminacion_db.sql
```

O manualmente:
```sql
ALTER TABLE usuarios ADD COLUMN contraseña_hash VARCHAR(255) NOT NULL;
```

### Error: "Decorators not found"

Verifica que `app/decorators.py` exista (no `backend/decorators.py`)

### Token no funciona en Swagger

- Verificar formato: `Bearer <token>` (con espacio)
- Verificar que el token no esté expirado
- Verificar que no haya caracteres extra

### CORS Error

Si ves error de CORS en console del navegador, verificar que CORS está configurado en `app/__init__.py`

### Base de datos no actualizada

Verificar con:
```sql
DESCRIBE usuarios;
```

Debe mostrar columnas:
- contraseña_hash
- rol (con default 'alumno')
- activo (con default 1)

## Paso Final: Confirmar Todo Funciona

Ejecutar este checklist completo:

```bash
# 1. BD conecta
mysql -u root -p iluminacion_db -e "SELECT COUNT(*) FROM usuarios;"

# 2. Python tiene PyJWT
python -c "import jwt; print('JWT OK')"

# 3. Server inicia
cd backend && timeout 5 python run.py || true

# 4. API responde
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"profesor@ejemplo.com","contraseña":"profesor123"}' \
  | grep -q "token" && echo "Login funciona!" || echo "Login falla!"
```

Si todos los pasos pasaron: ✅ **Sistema listo para usar**

## Contacto / Soporte

Si encuentras problemas:

1. Revisar los archivos de documentación
2. Verificar los logs del servidor
3. Ejecutar los tests de verificación
4. Revisar la estructura de archivos

## Documentación de Referencia

- [SISTEMA_ROLES.md](SISTEMA_ROLES.md) - Guía completa
- [ARQUITECTURA_ROLES.md](ARQUITECTURA_ROLES.md) - Diagramas y flujos
- [INSTALACION_RAPIDA.md](INSTALACION_RAPIDA.md) - Quick start
- [frontend/EJEMPLOS_INTEGRACION.ts](frontend/EJEMPLOS_INTEGRACION.ts) - Código React

---

**Última actualización**: 2026-06-12
**Versión**: 1.0
**Estado**: ✅ Listo para producción
