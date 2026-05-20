from app import db


class ConsumoEnergetico(db.Model):
    __tablename__ = 'consumo_energetico'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensores.id'), nullable=False)
    total_kwh = db.Column(db.Float, nullable=False)
    periodo_inicio = db.Column(db.Date, nullable=False)
    periodo_fin = db.Column(db.Date, nullable=False)
    creado_en = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    actualizado_en = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)
