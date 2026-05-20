from app.repositories.config_repository import ConfigRepository


class ConfigService:
    @staticmethod
    def get_configuration():
        return ConfigRepository.get_current()

    @staticmethod
    def update_configuration(config, payload):
        if 'modo_automatico' not in payload:
            raise ValueError('El modo automático debe especificarse.')
        if 'intensidad_led_default' in payload and payload['intensidad_led_default'] < 0:
            raise ValueError('La intensidad LED debe ser un número positivo.')
        return ConfigRepository.update(config, payload)
