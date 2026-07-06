from app.repositories.salon_repository import SalonRepository
from app.repositories.sensor_repository import SensorRepository
from app.utils.lighting import classify_lux_reading


class DashboardService:
    @staticmethod
    def get_latest_by_salon():
        # Usar orden por ID para que el dashboard muestre salones
        # en el mismo orden fijo que usa el ESP32 (por salon_id numérico)
        salones = SalonRepository.list_all_with_activity_ordered_by_id()
        dashboard = []

        for salon in salones:

            latest = SensorRepository.get_latest_by_salon(salon.id)

            lux_value = latest.lux if latest else None
            lux_minimo = salon.actividad.lux_minimo if salon.actividad else None
            lux_maximo = salon.actividad.lux_maximo if salon.actividad else None
            lighting = classify_lux_reading(lux_value, lux_minimo, lux_maximo)

            dashboard.append({
                'salon_id': salon.id,
                'nombre': salon.nombre,

                'actividad_id': salon.actividad_id,
                'actividad_nombre': salon.actividad_nombre,

                'lux': lux_value,

                'lux_minimo': lux_minimo,
                'lux_maximo': lux_maximo,

                'estado_iluminacion': lighting['estado_iluminacion'],
                'nivel_alerta': lighting['nivel_alerta'],

                'intensidad_led': latest.intensidad_led if latest else None,
                'consumo_energetico': latest.consumo_energetico if latest else None,
                'modo_automatico': latest.modo_automatico if latest else None,
            })

        return dashboard