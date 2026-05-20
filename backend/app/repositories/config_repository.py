from app.models.configuracion import Configuracion
from app import db


class ConfigRepository:
    @staticmethod
    def get_current():
        config = Configuracion.query.order_by(Configuracion.id.desc()).first()
        if not config:
            config = Configuracion()
            db.session.add(config)
            db.session.commit()
        return config

    @staticmethod
    def update(config, data):
        for key, value in data.items():
            setattr(config, key, value)
        db.session.commit()
        return config
