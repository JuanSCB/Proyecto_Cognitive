from typing import Any, Dict, Optional


def classify_lux_reading(lux: Optional[float], lux_minimo: Optional[float] = None, lux_maximo: Optional[float] = None) -> Dict[str, Any]:
    """Clasifica un nivel de lux de acuerdo con la lógica del firmware ESP32.

    Ignora los umbrales de la actividad para la lógica de clasificación.

    Retorna un diccionario con:
    - estado_iluminacion: 'Iluminación insuficiente', 'Iluminación adecuada', 'Iluminación excesiva' o 'Sin monitoreo'
    - nivel_alerta: 'verde' o 'rojo'
    - categoria: 'adecuado', 'insuficiente', 'excesivo' o 'sin_datos'
    """
    if lux is None:
        return {
            'estado_iluminacion': 'Sin monitoreo',
            'nivel_alerta': 'rojo',
            'categoria': 'sin_datos',
        }

    if lux <= 100:
        return {
            'estado_iluminacion': 'Iluminación insuficiente',
            'nivel_alerta': 'rojo',
            'categoria': 'insuficiente',
        }

    if lux <= 6000:
        return {
            'estado_iluminacion': 'Iluminación adecuada',
            'nivel_alerta': 'verde',
            'categoria': 'adecuado',
        }

    return {
        'estado_iluminacion': 'Iluminación excesiva',
        'nivel_alerta': 'rojo',
        'categoria': 'excesivo',
    }
