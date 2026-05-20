from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import config_model
from app.services.config_service import ConfigService

config_ns = Namespace('configuracion', description='Gestión de configuración del sistema')


@config_ns.route('')
class Configuration(Resource):
    @config_ns.marshal_with(config_model)
    def get(self):
        return ConfigService.get_configuration()

    @config_ns.expect(config_model, validate=True)
    @config_ns.marshal_with(config_model)
    def put(self):
        payload = config_ns.payload
        try:
            return ConfigService.update_configuration(ConfigService.get_configuration(), payload)
        except ValueError as error:
            abort(400, str(error))
