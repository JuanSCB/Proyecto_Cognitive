from app import db


class Actividad(db.Model):
    __tablename__ = 'actividades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    sensores = db.relationship('Sensor', backref='actividad', lazy=True)
    historial = db.relationship('HistorialIluminacion', backref='actividad', lazy=True)
