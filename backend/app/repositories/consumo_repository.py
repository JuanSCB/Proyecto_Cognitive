from app.models.consumo_energetico import ConsumoEnergetico


class ConsumptionRepository:
    @staticmethod
    def list_all():
        return ConsumoEnergetico.query.order_by(ConsumoEnergetico.creado_en.desc()).all()
