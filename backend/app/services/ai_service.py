from app import db
from app.models.salon import Salon
from app.models.sensor import Sensor
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico
from app.repositories.salon_repository import SalonRepository
from app.utils.ai_utils import generate_ollama_response


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

        actividad_nombre = salon.actividad.nombre if salon.actividad else None
        actividad_actual = actividad_nombre or (latest_sensor.actividad.nombre if latest_sensor and latest_sensor.actividad else None)

        lux_actual = latest_sensor.lux if latest_sensor else None
        lux_promedio = round(sum(item.lux for item in history_entries) / len(history_entries), 2) if history_entries else None
        intensidad_led = latest_sensor.intensidad_led if latest_sensor else None
        consumo_energetico = consumo_entry.total_kwh if consumo_entry else (latest_sensor.consumo_energetico if latest_sensor else None)
        modo = 'automático' if latest_sensor and latest_sensor.modo_automatico else 'manual' if latest_sensor else None
        fecha = None

        if latest_sensor and latest_sensor.registrado_en:
            fecha = latest_sensor.registrado_en.strftime('%Y-%m-%d %H:%M:%S')
        elif salon.actualizado_en:
            fecha = salon.actualizado_en.strftime('%Y-%m-%d %H:%M:%S')

        # Se construye el prompt con datos reales del salón y su historial.
        prompt = (
            "Eres un ingeniero experto en eficiencia energética y automatización.\n"
            "Analiza la siguiente información del sistema de iluminación inteligente.\n\n"
            f"Salón: {salon.nombre or 'No disponible'}\n"
            f"Actividad: {actividad_actual or 'No disponible'}\n"
            f"Modo: {modo or 'No disponible'}\n"
            f"Lux actual: {lux_actual if lux_actual is not None else 'No disponible'}\n"
            f"Lux promedio: {lux_promedio if lux_promedio is not None else 'No disponible'}\n"
            f"Intensidad LED: {intensidad_led if intensidad_led is not None else 'No disponible'}\n"
            f"Consumo energético: {consumo_energetico if consumo_energetico is not None else 'No disponible'}\n"
            f"Fecha: {fecha or 'No disponible'}\n\n"
            "Genera un reporte con el siguiente formato:\n"
            "1. Estado general del salón.\n"
            "2. Diagnóstico técnico.\n"
            "3. Posibles problemas detectados.\n"
            "4. Recomendaciones para optimizar iluminación y consumo energético.\n"
            "No inventes información.\n"
            "Si los datos no son suficientes indícalo.\n"
            "Responde máximo en seis líneas.\n"
            "Siempre responde en español."
        )

        analisis = generate_ollama_response(prompt)
        analisis = analisis or 'No fue posible generar un análisis con los datos disponibles.'

        return {
            'salon': salon.nombre,
            'analisis': analisis,
            'fecha': fecha or salon.actualizado_en.strftime('%Y-%m-%d %H:%M:%S') if salon.actualizado_en else None,
            'modelo': OLLAMA_MODEL,
        }
