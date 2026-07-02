from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def list_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user(user_id):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def create_user(payload):
        if not payload.get('nombre'):
            raise ValueError('El nombre es obligatorio.')
        if not payload.get('correo'):
            raise ValueError('El correo es obligatorio.')
        if not payload.get('contraseña_hash'):
            raise ValueError('La contraseña es obligatoria.')
        if not payload.get('rol'):
            raise ValueError('El rol es obligatorio.')
        
        # Validar rol
        if payload.get('rol') not in ['administrador', 'alumno']:
            raise ValueError('El rol debe ser "administrador" o "alumno".')
        
        return UserRepository.create(payload)

    @staticmethod
    def update_user(user, payload):
        if 'nombre' in payload and not payload['nombre']:
            raise ValueError('El nombre no puede estar vacío.')
        if 'correo' in payload and not payload['correo']:
            raise ValueError('El correo no puede estar vacío.')
        if 'rol' in payload and payload['rol'] not in ['administrador', 'alumno']:
            raise ValueError('El rol debe ser "administrador" o "alumno".')
        
        return UserRepository.update(user, payload)

    @staticmethod
    def delete_user(user):
        UserRepository.delete(user)
