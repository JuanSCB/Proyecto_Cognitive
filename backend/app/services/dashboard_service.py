from app.repositories.salon_repository import SalonRepository
from app.repositories.sensor_repository import SensorRepository


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

            # =====================================================
            # Clasificación de iluminación (igual que el ESP32)
            # =====================================================

            if lux_value is None:

                estado_iluminacion = 'Sin datos'
                nivel_alerta = 'rojo'

            elif lux_value <= 100:

                estado_iluminacion = 'Ambiente oscuro'
                nivel_alerta = 'rojo'

            elif lux_value <= 6000:

                estado_iluminacion = 'Ambiente con iluminación media'
                nivel_alerta = 'amarillo'

            else:

                estado_iluminacion = 'Ambiente muy iluminado'
                nivel_alerta = 'verde'

            dashboard.append({

                'salon_id': salon.id,
                'nombre': salon.nombre,

                'actividad_id': salon.actividad_id,
                'actividad_nombre': salon.actividad_nombre,

                'lux': lux_value,

                'lux_minimo': lux_minimo,
                'lux_maximo': lux_maximo,

                'estado_iluminacion': estado_iluminacion,
                'nivel_alerta': nivel_alerta,

                'intensidad_led': latest.intensidad_led if latest else None,
                'consumo_energetico': latest.consumo_energetico if latest else None,
                'modo_automatico': latest.modo_automatico if latest else None,

            })

        return dashboard