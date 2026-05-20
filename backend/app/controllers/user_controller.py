from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import user_model
from app.services.user_service import UserService

user_ns = Namespace('usuarios', description='Gestión de usuarios')


@user_ns.route('')
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        return UserService.list_users()

    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        try:
            return UserService.create_user(user_ns.payload), 201
        except ValueError as error:
            abort(400, str(error))


@user_ns.route('/<int:id>')
@user_ns.param('id', 'ID del usuario')
class UserItem(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, id):
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        return user

    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_model)
    def put(self, id):
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        try:
            return UserService.update_user(user, user_ns.payload)
        except ValueError as error:
            abort(400, str(error))

    def delete(self, id):
        user = UserService.get_user(id)
        if not user:
            abort(404, 'Usuario no encontrado')
        UserService.delete_user(user)
        return {'message': 'Usuario eliminado correctamente.'}, 200
