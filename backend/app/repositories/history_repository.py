from app.models.historial_iluminacion import HistorialIluminacion
from app.models.sensor import Sensor
from app import db


class HistoryRepository:
    @staticmethod
    def list_all():
        return HistorialIluminacion.query.order_by(HistorialIluminacion.registrado_en.desc()).all()

    @staticmethod
    def list_by_salon(salon_id):
        return (
            HistorialIluminacion.query
            .join(Sensor)
            .filter(Sensor.salon_id == salon_id)
            .order_by(HistorialIluminacion.registrado_en.desc())
            .all()
        )

    @staticmethod
    def query_range(start_date=None, end_date=None):
        query = HistorialIluminacion.query
        if start_date:
            query = query.filter(HistorialIluminacion.registrado_en >= start_date)
        if end_date:
            query = query.filter(HistorialIluminacion.registrado_en <= end_date)
        return query.order_by(HistorialIluminacion.registrado_en.desc()).all()
