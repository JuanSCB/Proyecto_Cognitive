from app.models.user import Usuario
from app import db


class UserRepository:
    @staticmethod
    def get_all():
        return Usuario.query.order_by(Usuario.creado_en.desc()).all()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(Usuario, user_id)

    @staticmethod
    def create(data):
        user = Usuario(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user, data):
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()
