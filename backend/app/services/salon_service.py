from app.repositories.salon_repository import SalonRepository
from app.repositories.sensor_repository import SensorRepository
from app.repositories.activity_repository import ActivityRepository
from app.utils.exceptions import BadRequestError, NotFoundError


class SalonService:
    @staticmethod
    def list_salons():
        return SalonRepository.list_all()

    @staticmethod
    def get_salon(salon_id):
        salon = SalonRepository.get_by_id(salon_id)
        if not salon:
            raise NotFoundError('Salón no encontrado.')
        return salon

    @staticmethod
    def create_salon(payload):
        if 'nombre' not in payload or not payload.get('nombre'):
            raise BadRequestError('El campo nombre es obligatorio.')

        actividad_id = payload.get('actividad_id')
        if actividad_id is None:
            raise BadRequestError('Debe seleccionar una actividad para crear el salón.')

        actividad = ActivityRepository.get_by_id(actividad_id)
        if not actividad:
            raise NotFoundError('actividad_id no existe.')

        return SalonRepository.create({
            'nombre': payload.get('nombre'),
            'ubicacion': payload.get('ubicacion'),
            'descripcion': payload.get('descripcion'),
            'actividad_id': actividad_id,
        })

    @staticmethod
    def update_salon(salon_id, payload):
        print('--- SalonService.update_salon ---')
        print('Payload:', payload)
        salon = SalonRepository.get_by_id(salon_id)
        print('Salón encontrado:', salon)
        if not salon:
            raise NotFoundError('Salón no encontrado.')

        actividad_id = payload['actividad_id'] if 'actividad_id' in payload else salon.actividad_id
        print('Actividad recibida:', payload.get('actividad_id'))
        if actividad_id is not None:
            actividad = ActivityRepository.get_by_id(actividad_id)
            if not actividad:
                raise NotFoundError('actividad_id no existe.')

        salon = SalonRepository.update(salon, {
            'nombre': payload.get('nombre', salon.nombre),
            'ubicacion': payload.get('ubicacion', salon.ubicacion),
            'descripcion': payload.get('descripcion', salon.descripcion),
            'actividad_id': actividad_id,
        })
        print('Retornando:', salon)
        return salon

    @staticmethod
    def delete_salon(salon_id):
        salon = SalonRepository.get_by_id(salon_id)
        if not salon:
            raise NotFoundError('Salón no encontrado.')
        SalonRepository.delete(salon)
        return {'message': 'Salón eliminado correctamente.'}

    @staticmethod
    def list_salon_sensors(salon_id):
        salon = SalonRepository.get_by_id(salon_id)
        if not salon:
            raise NotFoundError('Salón no encontrado.')
        return SensorRepository.list_by_salon(salon_id)
