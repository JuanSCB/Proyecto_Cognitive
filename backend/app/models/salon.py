from app import db


class Salon(db.Model):
    __tablename__ = 'salones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ubicacion = db.Column(db.String(150), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=True)
    creado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    sensores = db.relationship('Sensor', backref='salon', lazy=True, passive_deletes=True)
    actividad = db.relationship('Actividad', backref='salones', lazy=True)

    @property
    def actividad_nombre(self):
        return self.actividad.nombre if self.actividad else None
