from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from flask import current_app


def require_role(required_role):
    """
    Decorador que verifica que el usuario tenga el rol requerido.
    Requiere que se envíe un token JWT en el header 'Authorization'.
    
    Roles soportados:
    - 'administrador': acceso completo
    - 'alumno': solo lectura

    Uso:
    @app.route('/salones', methods=['POST'])
    @require_role('administrador')
    def crear_salon():
        ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print('===== REQUIRE_ROLE =====')
            print('METHOD:', request.method)
            print('PATH:', request.path)
            # Obtener el token del header Authorization (aceptar variantes)
            auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
            print('Authorization:', auth_header)
            print('SECRET_KEY:', current_app.config['SECRET_KEY'])

            # Soporte adicional: cabecera alternativa o query param/cookie (fallbacks)
            if not auth_header:
                auth_header = request.headers.get('X-Access-Token') or request.args.get('token') or request.cookies.get('token')

            if not auth_header:
                raise Exception('No Authorization header present')
            
            try:
                # Esperar formato "Bearer <token>" o simplemente el token
                parts = auth_header.split(' ')
                token = parts[1] if len(parts) > 1 else parts[0]
                print('TOKEN:', token)
                
                # Decodificar el token
                payload = jwt.decode(
                    token,
                    current_app.config.get('SECRET_KEY', 'dev-secret-key'),
                    algorithms=['HS256']
                )
                print('PAYLOAD:', payload)
                
                user_id = payload.get('user_id')
                user_role = payload.get('role')
                print('ROLE:', user_role)
                print('ENTRANDO AL ENDPOINT')
                
                # Verificar que el rol es válido
                if user_role not in ['administrador', 'alumno']:
                    raise Exception(f'El rol "{user_role}" no es válido')
                
                # Verificar que el usuario tiene el rol requerido
                if required_role == 'administrador' and user_role != 'administrador':
                    raise Exception('Se requiere rol de administrador para esta operación')
                
                # Pasar el ID y rol del usuario a la función
                kwargs['usuario_id'] = user_id
                kwargs['usuario_role'] = user_role
                
                return f(*args, **kwargs)
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise
        
        return decorated_function
    return decorator


def create_token(user_id, role, expires_in_hours=24):
    """
    Crea un token JWT para un usuario.
    
    Args:
        user_id: ID del usuario
        role: Rol del usuario ('administrador' o 'alumno')
        expires_in_hours: Horas hasta que expire el token
    
    Returns:
        Token JWT codificado
    """
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY', 'dev-secret-key'),
        algorithm='HS256'
    )
    
    return token


def verify_token(token):
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token: Token JWT
    
    Returns:
        Diccionario con user_id y role si es válido, None si no es válido
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('SECRET_KEY', 'dev-secret-key'),
            algorithms=['HS256']
        )
        return {
            'user_id': payload.get('user_id'),
            'role': payload.get('role')
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
