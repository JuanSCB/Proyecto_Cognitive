from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import activity_model
from app.services.activity_service import ActivityService
from app.decorators import require_role

activity_ns = Namespace('actividades', description='Gestión de actividades')


@activity_ns.route('')
class ActivityList(Resource):
    @activity_ns.marshal_list_with(activity_model)
    def get(self):
        """Obtener lista de actividades (Accesible para todos)"""
        return ActivityService.list_activities()

    @activity_ns.expect(activity_model, validate=True)
    @activity_ns.marshal_with(activity_model, code=201)
    @require_role('administrador')
    def post(self, usuario_id=None, usuario_role=None):
        """Crear nueva actividad (Solo administrador)"""
        payload = activity_ns.payload
        try:
            activity = ActivityService.create_activity(payload)
            return activity, 201
        except ValueError as error:
            abort(400, str(error))


@activity_ns.route('/<int:id>')
@activity_ns.param('id', 'ID de la actividad')
class ActivityItem(Resource):
    @activity_ns.marshal_with(activity_model)
    def get(self, id):
        """Obtener detalles de una actividad (Accesible para todos)"""
        activity = ActivityService.get_activity(id)
        if not activity:
            abort(404, 'Actividad no encontrada')
        return activity

    @activity_ns.expect(activity_model, validate=True)
    @activity_ns.marshal_with(activity_model)
    @require_role('administrador')
    def put(self, id, usuario_id=None, usuario_role=None):
        """Actualizar actividad (Solo administrador)"""
        activity = ActivityService.get_activity(id)
        if not activity:
            abort(404, 'Actividad no encontrada')
        try:
            return ActivityService.update_activity(activity, activity_ns.payload)
        except ValueError as error:
            abort(400, str(error))

    @require_role('administrador')
    def delete(self, id, usuario_id=None, usuario_role=None):
        """Eliminar actividad (Solo administrador)"""
        activity = ActivityService.get_activity(id)
        if not activity:
            abort(404, 'Actividad no encontrada')
        ActivityService.delete_activity(activity)
        return {'message': 'Actividad eliminada correctamente.'}, 200
