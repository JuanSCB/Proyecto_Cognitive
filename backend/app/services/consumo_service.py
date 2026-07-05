from app.repositories.consumo_repository import ConsumptionRepository


class ConsumptionService:
    @staticmethod
    def list_consumption(salon_id=None):
        return ConsumptionRepository.list_all(salon_id)
