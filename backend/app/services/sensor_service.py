from datetime import date
from app.repositories.sensor_repository import SensorRepository
from app.config_defaults import DEFAULT_UMBRAL_LUX, DEFAULT_INTENSIDAD_LED_DEFAULT
from app.repositories.history_repository import HistoryRepository
from app.repositories.activity_repository import ActivityRepository
from app.repositories.salon_repository import SalonRepository
from app.utils.exceptions import BadRequestError, NotFoundError


class SensorService:
    @staticmethod
    def list_sensors(page=1, limit=20):
        return SensorRepository.list_paginated(page, limit)

    @staticmethod
    def register_reading(payload):
        required = ['lux', 'intensidad_led', 'consumo_energetico', 'modo_automatico']
        for field in required:
            if field not in payload:
                raise BadRequestError(f'El campo {field} es obligatorio.')

        lux = payload.get('lux')
        intensidad_led = payload.get('intensidad_led')
        consumo_energetico = payload.get('consumo_energetico')
        actividad_id = payload.get('actividad_id')

        if lux is None or lux < 0:
            raise BadRequestError('lux no puede ser negativo.')
        if intensidad_led is None or intensidad_led < 0 or intensidad_led > 100:
            raise BadRequestError('intensidad_led debe estar entre 0 y 100.')
        if consumo_energetico is None or consumo_energetico < 0:
            raise BadRequestError('consumo_energetico no puede ser negativo.')

        if actividad_id is not None:
            actividad = ActivityRepository.get_by_id(actividad_id)
            if not actividad:
                raise NotFoundError('actividad_id no existe.')

        salon_id = payload.get('salon_id')
        if salon_id is None:
            raise BadRequestError('salon_id es obligatorio.')

        salon = SalonRepository.get_by_id(salon_id)
        if not salon:
            raise NotFoundError('salon_id no existe.')

        # Use configured defaults (configuration CRUD removed)
        config_umbral = DEFAULT_UMBRAL_LUX
        config_intensidad_default = DEFAULT_INTENSIDAD_LED_DEFAULT
        data = {
            'lux': lux,
            'intensidad_led': intensidad_led,
            'consumo_energetico': consumo_energetico,
            'modo_automatico': payload.get('modo_automatico'),
            'actividad_id': actividad_id,
            'salon_id': salon_id,
        }

        if payload.get('modo_automatico') and lux < config_umbral:
            data['intensidad_led'] = max(0, config_intensidad_default)

        sensor = SensorRepository.create(data)
        SensorRepository.create_history(sensor)
        SensorRepository.create_consumption(sensor, date.today(), date.today())
        return sensor

    @staticmethod
    def get_latest_sensor():
        return SensorRepository.get_latest()
