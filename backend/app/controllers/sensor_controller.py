from flask import request
from flask_restx import Namespace, Resource, abort
from app.schemas.swagger_models import sensor_input, sensor_model, paginated_sensor_model
from app.services.sensor_service import SensorService
from app.utils.exceptions import BadRequestError
from app.decorators import require_role

sensor_ns = Namespace('sensores', description='Registro y lectura de datos del sensor')


@sensor_ns.route('')
class SensorList(Resource):
    @sensor_ns.marshal_with(paginated_sensor_model)
    @sensor_ns.param('page', 'Página de resultados', type=int)
    @sensor_ns.param('limit', 'Cantidad de resultados por página', type=int)
    def get(self):
        """Obtener lista de lecturas de sensores (Accesible para todos)"""
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
        except (TypeError, ValueError):
            raise BadRequestError('page y limit deben ser números enteros.')

        if page < 1 or limit < 1:
            raise BadRequestError('page y limit deben ser mayores a 0.')

        return SensorService.list_sensors(page, limit)

    @sensor_ns.expect(sensor_input, validate=True)
    @sensor_ns.marshal_with(sensor_model, code=201)
    @require_role('profesor')
    def post(self, usuario_id=None, usuario_role=None):
        """Registrar lectura de sensor (Solo profesor)"""
        payload = sensor_ns.payload
        sensor = SensorService.register_reading(payload)
        return sensor, 201


@sensor_ns.route('/latest')
class SensorLatest(Resource):
    @sensor_ns.marshal_with(sensor_model)
    def get(self):
        """Obtener última lectura de sensor (Accesible para todos)"""
        latest = SensorService.get_latest_sensor()
        if not latest:
            abort(404, 'No se encontró ningún registro de sensor.')
        return latest
