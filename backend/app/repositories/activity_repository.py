from app.models.activity import Actividad
from app import db


class ActivityRepository:
    @staticmethod
    def get_all():
        return Actividad.query.order_by(Actividad.creado_en.desc()).all()

    @staticmethod
    def get_by_id(activity_id):
        return db.session.get(Actividad, activity_id)

    @staticmethod
    def get_by_name(name):
        if not name:
            return None
        return Actividad.query.filter(db.func.lower(Actividad.nombre) == name.strip().lower()).first()

    @staticmethod
    def create(data):
        activity = Actividad(**data)
        db.session.add(activity)
        db.session.commit()
        return activity

    @staticmethod
    def update(activity, data):
        for key, value in data.items():
            setattr(activity, key, value)
        db.session.commit()
        return activity

    @staticmethod
    def delete(activity):
        db.session.delete(activity)
        db.session.commit()
