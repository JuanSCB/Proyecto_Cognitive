from app.models.consumo_energetico import ConsumoEnergetico
from app.models.sensor import Sensor


class ConsumptionRepository:
    @staticmethod
    def list_all(salon_id=None):
        query = ConsumoEnergetico.query
        if salon_id is not None:
            query = query.join(Sensor).filter(Sensor.salon_id == salon_id)
        return query.order_by(ConsumoEnergetico.creado_en.desc()).all()
