from app import db


class Configuracion(db.Model):
    __tablename__ = 'configuracion'

    id = db.Column(db.Integer, primary_key=True)
    modo_automatico = db.Column(db.Boolean, nullable=False, default=True)
    intensidad_led_default = db.Column(db.Integer, nullable=False, default=70)
    umbral_lux = db.Column(db.Integer, nullable=False, default=300)
    max_consumo = db.Column(db.Float, nullable=False, default=100.0)
    creado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
