class HealthService:
    @staticmethod
    def get_health():
        return {
            'status': 'ok',
            'service': 'Sistema Inteligente de Iluminación',
            'version': '1.0'
        }
