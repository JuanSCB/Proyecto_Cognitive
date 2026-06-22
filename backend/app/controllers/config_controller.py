from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import config_model
from app.services.config_service import ConfigService
from app.decorators import require_role

config_ns = Namespace('configuracion', description='Gestión de configuración del sistema')


@config_ns.route('')
class Configuration(Resource):
    @config_ns.marshal_with(config_model)
    def get(self):
        """Obtener configuración del sistema (Accesible para todos)"""
        return ConfigService.get_configuration()

    @config_ns.expect(config_model, validate=True)
    @config_ns.marshal_with(config_model)
    @require_role('profesor')
    def put(self, usuario_id=None, usuario_role=None):
        """Actualizar configuración del sistema (Solo profesor)"""
        payload = config_ns.payload
        try:
            return ConfigService.update_configuration(ConfigService.get_configuration(), payload)
        except ValueError as error:
            abort(400, str(error))
