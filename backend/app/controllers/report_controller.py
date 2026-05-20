from flask_restx import Namespace, Resource
from app.schemas.swagger_models import (
    report_model,
    sensor_model,
    average_lux_model,
    total_consumo_model,
    statistics_model,
)
from app.services.report_service import ReportService

report_ns = Namespace('reportes', description='Reportes e historial de iluminación')


@report_ns.route('')
class Report(Resource):
    @report_ns.marshal_with(report_model)
    def get(self):
        report_data = ReportService.get_report()
        if report_data['ultimo_registro'] is None:
            return {**report_data, 'ultimo_registro': {}}, 200
        return report_data


@report_ns.route('/historial')
class History(Resource):
    @report_ns.marshal_list_with(sensor_model)
    def get(self):
        return ReportService.get_history()


@report_ns.route('/promedio-lux')
class AverageLux(Resource):
    @report_ns.marshal_with(average_lux_model)
    def get(self):
        return ReportService.get_average_lux()


@report_ns.route('/consumo-total')
class TotalConsumption(Resource):
    @report_ns.marshal_with(total_consumo_model)
    def get(self):
        return ReportService.get_total_consumption()


@report_ns.route('/estadisticas')
class Statistics(Resource):
    @report_ns.marshal_with(statistics_model)
    def get(self):
        return ReportService.get_statistics()
