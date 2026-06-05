from flask_restx import Namespace, Resource
from app.schemas.swagger_models import dashboard_salon_model
from app.services.dashboard_service import DashboardService

dashboard_ns = Namespace('dashboard', description='Dashboard y últimas lecturas por salón')


@dashboard_ns.route('/salones')
class DashboardSalones(Resource):
    @dashboard_ns.marshal_list_with(dashboard_salon_model)
    def get(self):
        return DashboardService.get_latest_by_salon()
