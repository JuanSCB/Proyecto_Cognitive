from app import db
from app.models.salon import Salon
from sqlalchemy.orm import joinedload


class SalonRepository:
    @staticmethod
    def list_all():
        return Salon.query.order_by(Salon.nombre).all()

    @staticmethod
    def list_all_with_activity():
        return Salon.query.options(joinedload(Salon.actividad)).order_by(Salon.nombre).all()

    @staticmethod
    def list_all_with_activity_ordered_by_id():
        return Salon.query.options(joinedload(Salon.actividad)).order_by(Salon.id).all()

    @staticmethod
    def get_by_id(salon_id):
        return db.session.get(Salon, salon_id, options=[joinedload(Salon.actividad)])

    @staticmethod
    def create(data):
        salon = Salon(**data)
        db.session.add(salon)
        db.session.commit()
        return salon

    @staticmethod
    def update(salon, data):
        for key, value in data.items():
            setattr(salon, key, value)
        db.session.commit()
        return salon

    @staticmethod
    def delete(salon):
        db.session.delete(salon)
        db.session.commit()
