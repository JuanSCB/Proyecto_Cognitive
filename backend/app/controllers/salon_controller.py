from flask_restx import Namespace, Resource
from app.schemas.swagger_models import salon_input, salon_update_input, salon_model, sensor_model
from app.services.salon_service import SalonService

salon_ns = Namespace('salones', description='Gestión de salones')


@salon_ns.route('')
class SalonList(Resource):
    @salon_ns.marshal_list_with(salon_model)
    def get(self):
        return SalonService.list_salons()

    @salon_ns.expect(salon_input, validate=True)
    @salon_ns.marshal_with(salon_model, code=201)
    def post(self):
        payload = salon_ns.payload
        salon = SalonService.create_salon(payload)
        return salon, 201


@salon_ns.route('/<int:id>')
class SalonDetail(Resource):
    @salon_ns.marshal_with(salon_model)
    def get(self, id):
        return SalonService.get_salon(id)

    @salon_ns.expect(salon_update_input, validate=False)
    @salon_ns.marshal_with(salon_model)
    def put(self, id):
        payload = salon_ns.payload
        return SalonService.update_salon(id, payload)

    def delete(self, id):
        return SalonService.delete_salon(id)


@salon_ns.route('/<int:id>/sensores')
class SalonSensors(Resource):
    @salon_ns.marshal_list_with(sensor_model)
    def get(self, id):
        return SalonService.list_salon_sensors(id)
