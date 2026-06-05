from datetime import date
from app.models.sensor import Sensor
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico
from app import db


class SensorRepository:
    @staticmethod
    def list_all():
        return Sensor.query.order_by(Sensor.registrado_en.desc()).all()

    @staticmethod
    def list_paginated(page, limit):
        query = Sensor.query.order_by(Sensor.registrado_en.desc())
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return {'items': items, 'page': page, 'limit': limit, 'total': total}

    @staticmethod
    def list_by_salon(salon_id):
        return Sensor.query.filter_by(salon_id=salon_id).order_by(Sensor.registrado_en.desc()).all()

    @staticmethod
    def get_latest_by_salon(salon_id):
        return Sensor.query.filter_by(salon_id=salon_id).order_by(Sensor.registrado_en.desc()).first()

    @staticmethod
    def create(data):
        sensor = Sensor(**data)
        db.session.add(sensor)
        db.session.commit()
        return sensor

    @staticmethod
    def create_history(sensor):
        history = HistorialIluminacion(
            sensor_id=sensor.id,
            lux=sensor.lux,
            intensidad_led=sensor.intensidad_led,
            consumo_energetico=sensor.consumo_energetico,
            modo_automatico=sensor.modo_automatico,
            actividad_id=sensor.actividad_id,
        )
        db.session.add(history)
        db.session.commit()
        return history

    @staticmethod
    def create_consumption(sensor, period_start, period_end):
        summary = ConsumoEnergetico(
            sensor_id=sensor.id,
            total_kwh=sensor.consumo_energetico,
            periodo_inicio=period_start,
            periodo_fin=period_end,
        )
        db.session.add(summary)
        db.session.commit()
        return summary

    @staticmethod
    def get_latest():
        return Sensor.query.order_by(Sensor.registrado_en.desc()).first()
