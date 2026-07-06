from flask_restx import Namespace, Resource
from flask import request, current_app
from app.schemas.swagger_models import salon_input, salon_update_input, salon_model, sensor_model
from app.services.salon_service import SalonService
from app.decorators import require_role

salon_ns = Namespace('salones', description='Gestión de salones')


@salon_ns.route('')
class SalonList(Resource):
    @salon_ns.marshal_list_with(salon_model)
    def get(self):
        """Obtener lista de salones (Accesible para todos)"""
        return SalonService.list_salons()

    @salon_ns.expect(salon_input, validate=True)
    @salon_ns.marshal_with(salon_model, code=201)
    @require_role('administrador')
    def post(self, usuario_id=None, usuario_role=None):
        """Crear nuevo salón (Solo administrador)"""
        payload = salon_ns.payload
        salon = SalonService.create_salon(payload)
        return salon, 201


@salon_ns.route('/<int:id>')
class SalonDetail(Resource):
    @salon_ns.marshal_with(salon_model)
    def get(self, id):
        """Obtener detalles de un salón (Accesible para todos)"""
        return SalonService.get_salon(id)

    @salon_ns.expect(salon_update_input, validate=False)
    @salon_ns.marshal_with(salon_model)
    # @require_role('administrador')
    def put(self, id, usuario_id=None, usuario_role=None):
        """Actualizar salón (Solo administrador)"""
        # Diagnostic: print headers to confirm Authorization arrived at backend
        try:
            # print raw headers for quick diagnostics (temporary)
            print('--- PUT /api/salones/{id} headers ---')
            print(request.headers)
            current_app.logger.debug('PUT /api/salones/%s headers: %s', id, dict(request.headers))
        except Exception:
            pass

        payload = salon_ns.payload
        return SalonService.update_salon(id, payload)

    @require_role('administrador')
    def delete(self, id, usuario_id=None, usuario_role=None):
        """Eliminar salón (Solo administrador)"""
        return SalonService.delete_salon(id)


@salon_ns.route('/<int:id>/sensores')
class SalonSensors(Resource):
    @salon_ns.marshal_list_with(sensor_model)
    def get(self, id):
        """Obtener sensores de un salón (Accesible para todos)"""
        return SalonService.list_salon_sensors(id)
