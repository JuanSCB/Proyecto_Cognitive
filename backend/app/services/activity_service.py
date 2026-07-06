from app.repositories.activity_repository import ActivityRepository
from app.utils.exceptions import BadRequestError, ConflictError


class ActivityService:
    @staticmethod
    def list_activities():
        return ActivityRepository.get_all()

    @staticmethod
    def get_activity(activity_id):
        return ActivityRepository.get_by_id(activity_id)

    @staticmethod
    def create_activity(payload):
        nombre = payload.get('nombre', '').strip()
        if not nombre:
            raise BadRequestError('El nombre de la actividad es requerido.')

        lux_minimo = payload.get('lux_minimo')
        lux_maximo = payload.get('lux_maximo')

        if lux_minimo is None:
            lux_minimo = 100
        if lux_maximo is None:
            lux_maximo = 6000

        try:
            lux_minimo = int(lux_minimo)
            lux_maximo = int(lux_maximo)
        except (TypeError, ValueError):
            raise BadRequestError('lux_minimo y lux_maximo deben ser valores numéricos válidos.')

        if lux_minimo < 0:
            raise BadRequestError('lux_minimo debe ser mayor o igual a 0.')

        if lux_maximo <= lux_minimo:
            raise BadRequestError('lux_maximo debe ser mayor que lux_minimo.')

        existing = ActivityRepository.get_by_name(nombre)
        if existing:
            raise ConflictError('Ya existe una actividad con ese nombre.')

        return ActivityRepository.create({
            'nombre': nombre,
            'descripcion': payload.get('descripcion'),
            'lux_minimo': lux_minimo,
            'lux_maximo': lux_maximo,
        })

    @staticmethod
    def update_activity(activity, payload):
        nombre = payload.get('nombre', '').strip()
        if not nombre:
            raise BadRequestError('El nombre de la actividad es requerido.')

        existing = ActivityRepository.get_by_name(nombre)
        if existing and existing.id != activity.id:
            raise ConflictError('Ya existe una actividad con ese nombre.')

        return ActivityRepository.update(activity, {
            'nombre': nombre,
            'descripcion': payload.get('descripcion'),
            'lux_minimo': payload.get('lux_minimo'),
            'lux_maximo': payload.get('lux_maximo')
        })

    @staticmethod
    def delete_activity(activity):
        ActivityRepository.delete(activity)
