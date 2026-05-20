from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import sensor_model
from app.services.report_service import ReportService

historial_ns = Namespace('historial', description='Consulta de historial de iluminación')


@historial_ns.route('')
class Historial(Resource):
    @historial_ns.marshal_list_with(sensor_model)
    @historial_ns.param('start_date', 'Fecha de inicio en formato YYYY-MM-DD')
    @historial_ns.param('end_date', 'Fecha de fin en formato YYYY-MM-DD')
    def get(self):
        try:
            start_date = self.parse_date(request.args.get('start_date'))
            end_date = self.parse_date(request.args.get('end_date'))
        except ValueError as error:
            abort(400, str(error))
        return ReportService.get_history(start_date, end_date)

    @staticmethod
    def parse_date(value):
        if not value:
            return None
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Formato de fecha inválido. Use YYYY-MM-DD.')
