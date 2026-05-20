from flask_restx import Namespace, Resource
from app.schemas.swagger_models import health_model
from app.services.health_service import HealthService

health_ns = Namespace('health', description='Chequeo de salud del API')


@health_ns.route('')
class HealthCheck(Resource):
    @health_ns.marshal_with(health_model)
    def get(self):
        return HealthService.get_health()
