from app.repositories.salon_repository import SalonRepository
from app.repositories.sensor_repository import SensorRepository


class DashboardService:
    @staticmethod
    def get_latest_by_salon():
        salones = SalonRepository.list_all_with_activity()
        dashboard = []
        for salon in salones:
            latest = SensorRepository.get_latest_by_salon(salon.id)
            lux_value = latest.lux if latest else None
            lux_minimo = salon.actividad.lux_minimo if salon.actividad else None
            lux_maximo = salon.actividad.lux_maximo if salon.actividad else None

            if lux_value is None or lux_minimo is None or lux_maximo is None:
                estado_iluminacion = 'Sin datos'
            elif lux_value < lux_minimo:
                estado_iluminacion = 'Insuficiente'
            elif lux_value <= lux_maximo:
                estado_iluminacion = 'Adecuada'
            else:
                estado_iluminacion = 'Excesiva'

            if estado_iluminacion in ['Insuficiente', 'Excesiva', 'Sin datos']:
                nivel_alerta = 'rojo'
            elif estado_iluminacion == 'Adecuada':
                rango = lux_maximo - lux_minimo
                proximidad_inferior = lux_minimo + rango * 0.1
                proximidad_superior = lux_maximo - rango * 0.1
                if lux_value <= proximidad_inferior or lux_value >= proximidad_superior:
                    nivel_alerta = 'amarillo'
                else:
                    nivel_alerta = 'verde'
            else:
                nivel_alerta = 'rojo'

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
