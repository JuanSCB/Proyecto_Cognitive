from app import db


class HistorialIluminacion(db.Model):
    __tablename__ = 'historial_iluminacion'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    lux = db.Column(db.Float, nullable=False)
    intensidad_led = db.Column(db.Integer, nullable=False)
    consumo_energetico = db.Column(db.Float, nullable=False)
    modo_automatico = db.Column(db.Boolean, nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=True)
    registrado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    creado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
