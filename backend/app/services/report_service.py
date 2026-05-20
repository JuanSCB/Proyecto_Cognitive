from app.repositories.history_repository import HistoryRepository
from app.repositories.sensor_repository import SensorRepository


class ReportService:
    @staticmethod
    def get_report():
        historial = HistoryRepository.list_all()
        ultimo = SensorRepository.get_latest()
        energia_total = sum(item.consumo_energetico for item in historial)

        return {
            'total_registros': len(historial),
            'energia_total': energia_total,
            'ultimo_registro': ultimo
        }

    @staticmethod
    def get_history(start_date=None, end_date=None):
        return HistoryRepository.query_range(start_date, end_date)

    @staticmethod
    def get_average_lux():
        historial = HistoryRepository.list_all()
        if not historial:
            return {'promedio_lux': 0.0, 'cantidad_registros': 0}
        promedio = sum(item.lux for item in historial) / len(historial)
        return {'promedio_lux': round(promedio, 2), 'cantidad_registros': len(historial)}

    @staticmethod
    def get_total_consumption():
        historial = HistoryRepository.list_all()
        total = sum(item.consumo_energetico for item in historial)
        return {'total_consumo': round(total, 2)}

    @staticmethod
    def get_statistics():
        historial = HistoryRepository.list_all()
        ultimo = SensorRepository.get_latest()
        cantidad = len(historial)
        if cantidad == 0:
            return {
                'promedio_lux': 0.0,
                'promedio_intensidad_led': 0.0,
                'total_consumo_energetico': 0.0,
                'cantidad_registros': 0,
                'ultimo_registro': None,
            }

        promedio_lux = sum(item.lux for item in historial) / cantidad
        promedio_intensidad_led = sum(item.intensidad_led for item in historial) / cantidad
        total_consumo = sum(item.consumo_energetico for item in historial)

        return {
            'promedio_lux': round(promedio_lux, 2),
            'promedio_intensidad_led': round(promedio_intensidad_led, 2),
            'total_consumo_energetico': round(total_consumo, 2),
            'cantidad_registros': cantidad,
            'ultimo_registro': ultimo,
        }
