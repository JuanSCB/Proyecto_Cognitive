from flask_restx import Namespace, Resource, fields
from app.models.user import Usuario
from app import db
from app.decorators import create_token
from flask import request

auth_ns = Namespace('auth', description='Autenticación y autorización')

# Modelos para Swagger
login_model = auth_ns.model('Login', {
    'correo': fields.String(required=True, description='Correo del usuario'),
    'contraseña': fields.String(required=True, description='Contraseña del usuario')
})

token_response_model = auth_ns.model('TokenResponse', {
    'token': fields.String(description='JWT token'),
    'usuario': fields.Nested(auth_ns.model('UsuarioInfo', {
        'id': fields.Integer,
        'nombre': fields.String,
        'correo': fields.String,
        'rol': fields.String
    })),
    'message': fields.String(description='Mensaje de respuesta')
})

error_response_model = auth_ns.model('ErrorResponse', {
    'error': fields.String,
    'message': fields.String
})


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login exitoso', token_response_model)
    @auth_ns.response(401, 'Credenciales inválidas', error_response_model)
    def post(self):
        """Inicia sesión y retorna un token JWT"""
        payload = request.get_json()
        correo = payload.get('correo')
        contraseña = payload.get('contraseña')
        
        if not correo or not contraseña:
            auth_ns.abort(400, 'Correo y contraseña son requeridos')
        
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if not usuario or not usuario.check_password(contraseña):
            auth_ns.abort(401, 'Correo o contraseña inválidos')
        
        if not usuario.activo:
            auth_ns.abort(401, 'Usuario inactivo')
        
        # Crear token JWT
        token = create_token(usuario.id, usuario.rol)
        
        return {
            'token': token,
            'usuario': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'rol': usuario.rol
            },
            'message': f'Bienvenido {usuario.nombre}'
        }, 200


@auth_ns.route('/register')
class Register(Resource):
    register_model = auth_ns.model('Register', {
        'nombre': fields.String(required=True, description='Nombre completo'),
        'correo': fields.String(required=True, description='Correo del usuario'),
        'contraseña': fields.String(required=True, description='Contraseña'),
        'rol': fields.String(required=False, default='alumno', description='Rol (profesor o alumno)')
    })
    
    @auth_ns.expect(register_model, validate=True)
    @auth_ns.response(201, 'Usuario registrado', token_response_model)
    @auth_ns.response(400, 'Error en el registro', error_response_model)
    def post(self):
        """Registra un nuevo usuario"""
        payload = request.get_json()
        
        nombre = payload.get('nombre', '').strip()
        correo = payload.get('correo', '').strip()
        contraseña = payload.get('contraseña', '').strip()
        rol = payload.get('rol', 'alumno').lower()
        
        # Validaciones
        if not nombre or not correo or not contraseña:
            auth_ns.abort(400, 'Nombre, correo y contraseña son requeridos')
        
        if len(contraseña) < 6:
            auth_ns.abort(400, 'La contraseña debe tener al menos 6 caracteres')
        
        if rol not in ['profesor', 'alumno']:
            auth_ns.abort(400, 'Rol inválido. Usar "profesor" o "alumno"')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(correo=correo).first():
            auth_ns.abort(400, 'El correo ya está registrado')
        
        # Crear nuevo usuario
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            rol=rol
        )
        usuario.set_password(contraseña)
        
        db.session.add(usuario)
        db.session.commit()
        
        # Crear token JWT
        token = create_token(usuario.id, usuario.rol)
        
        return {
            'token': token,
            'usuario': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'rol': usuario.rol
            },
            'message': f'Usuario {usuario.nombre} registrado exitosamente'
        }, 201
