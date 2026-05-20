from flask_restx import Namespace, Resource
from app.schemas.swagger_models import consumption_model
from app.services.consumo_service import ConsumptionService

consumo_ns = Namespace('consumo', description='Gestión de consumo energético')


@consumo_ns.route('')
class ConsumptionList(Resource):
    @consumo_ns.marshal_list_with(consumption_model)
    def get(self):
        return ConsumptionService.list_consumption()
