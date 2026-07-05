from app import db
from app.models.salon import Salon
from app.models.sensor import Sensor
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico
from app.repositories.salon_repository import SalonRepository
from app.utils.ai_utils import build_lumibot_analysis_prompt, generate_ollama_response, OLLAMA_MODEL


class AIService:
    @staticmethod
    def analyze_room(salon_id):
        salon = SalonRepository.get_by_id(salon_id)
        if not salon:
            raise ValueError('Salón no encontrado')

        latest_sensor = (
            Sensor.query.filter_by(salon_id=salon_id)
            .order_by(Sensor.registrado_en.desc())
            .first()
        )

        history_entries = (
            db.session.query(HistorialIluminacion)
            .join(Sensor)
            .filter(Sensor.salon_id == salon_id)
            .order_by(HistorialIluminacion.registrado_en.desc())
            .all()
        )

        consumo_entry = (
            db.session.query(ConsumoEnergetico)
            .join(Sensor)
            .filter(Sensor.salon_id == salon_id)
            .order_by(ConsumoEnergetico.creado_en.desc())
            .first()
        )

        fecha = None
        if latest_sensor and latest_sensor.registrado_en:
            fecha = latest_sensor.registrado_en.strftime('%Y-%m-%d %H:%M:%S')
        elif salon.actualizado_en:
            fecha = salon.actualizado_en.strftime('%Y-%m-%d %H:%M:%S')

        prompt = build_lumibot_analysis_prompt(salon, latest_sensor, history_entries, consumo_entry)

        analisis = generate_ollama_response(prompt)
        analisis = analisis or 'No fue posible generar un análisis con los datos disponibles.'

        return {
            'salon': salon.nombre,
            'analisis': analisis,
            'fecha': fecha,
            'modelo': OLLAMA_MODEL,
        }
