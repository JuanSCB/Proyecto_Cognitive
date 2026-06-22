from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import user_model
from app.services.user_service import UserService
from app.decorators import require_role

user_ns = Namespace('usuarios', description='Gestión de usuarios')


@user_ns.route('')
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    @require_role('profesor')
    def get(self, usuario_id=None, usuario_role=None):
        """Obtener lista de usuarios (Solo profesor)"""
        return UserService.list_users()

    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_model, code=201)
    @require_role('profesor')
    def post(self, usuario_id=None, usuario_role=None):
        """Crear nuevo usuario (Solo profesor)"""
        try:
            return UserService.create_user(user_ns.payload), 201
        except ValueError as error:
            abort(400, str(error))


@user_ns.route('/<int:id>')
@user_ns.param('id', 'ID del usuario')
class UserItem(Resource):
    @user_ns.marshal_with(user_model)
    @require_role('profesor')
    def get(self, id, usuario_id=None, usuario_role=None):
        """Obtener detalles de usuario (Solo profesor)"""
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        return user

    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_model)
    @require_role('profesor')
    def put(self, id, usuario_id=None, usuario_role=None):
        """Actualizar usuario (Solo profesor)"""
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        try:
            return UserService.update_user(user, user_ns.payload)
        except ValueError as error:
            abort(400, str(error))

    @require_role('profesor')
    def delete(self, id, usuario_id=None, usuario_role=None):
        """Eliminar usuario (Solo profesor)"""
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        UserService.delete_user(user)
        return {'message': 'Usuario eliminado correctamente.'}, 200
