from app.repositories.consumo_repository import ConsumptionRepository


class ConsumptionService:
    @staticmethod
    def list_consumption():
        return ConsumptionRepository.list_all()
