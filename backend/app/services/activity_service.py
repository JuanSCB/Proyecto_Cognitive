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

        existing = ActivityRepository.get_by_name(nombre)
        if existing:
            raise ConflictError('Ya existe una actividad con ese nombre.')

        return ActivityRepository.create({'nombre': nombre, 'descripcion': payload.get('descripcion')})

    @staticmethod
    def update_activity(activity, payload):
        nombre = payload.get('nombre', '').strip()
        if not nombre:
            raise BadRequestError('El nombre de la actividad es requerido.')

        existing = ActivityRepository.get_by_name(nombre)
        if existing and existing.id != activity.id:
            raise ConflictError('Ya existe una actividad con ese nombre.')

        return ActivityRepository.update(activity, {'nombre': nombre, 'descripcion': payload.get('descripcion')})

    @staticmethod
    def delete_activity(activity):
        ActivityRepository.delete(activity)
