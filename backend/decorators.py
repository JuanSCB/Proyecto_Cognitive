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
            # Obtener el token del header Authorization
            auth_header = request.headers.get('Authorization', '')
            
            if not auth_header:
                return jsonify({
                    'error': 'No autorizado',
                    'message': 'Se requiere token de autenticación'
                }), 401
            
            try:
                # Esperar formato "Bearer <token>"
                token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
                
                # Decodificar el token
                payload = jwt.decode(
                    token,
                    current_app.config.get('SECRET_KEY', 'dev-secret-key'),
                    algorithms=['HS256']
                )
                
                user_id = payload.get('user_id')
                user_role = payload.get('role')
                
                # Verificar que el rol es válido
                if user_role not in ['administrador', 'alumno']:
                    return jsonify({
                        'error': 'Rol inválido',
                        'message': f'El rol "{user_role}" no es válido'
                    }), 403
                
                # Verificar que el usuario tiene el rol requerido
                if required_role == 'administrador' and user_role != 'administrador':
                    return jsonify({
                        'error': 'Acceso denegado',
                        'message': 'Se requiere rol de administrador para esta operación'
                    }), 403
                
                # Pasar el ID y rol del usuario a la función
                kwargs['usuario_id'] = user_id
                kwargs['usuario_role'] = user_role
                
                return f(*args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                return jsonify({
                    'error': 'Token expirado',
                    'message': 'El token de autenticación ha expirado'
                }), 401
            except jwt.InvalidTokenError:
                return jsonify({
                    'error': 'Token inválido',
                    'message': 'El token de autenticación es inválido'
                }), 401
            except Exception as e:
                return jsonify({
                    'error': 'Error de autenticación',
                    'message': str(e)
                }), 401
        
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
