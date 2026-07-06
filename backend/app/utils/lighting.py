from typing import Any, Dict, Optional


def classify_lux_reading(lux: Optional[float], lux_minimo: Optional[float] = None, lux_maximo: Optional[float] = None) -> Dict[str, Any]:
    """Clasifica un nivel de lux con umbrales de actividad o umbrales por defecto.

    Retorna un diccionario con:
    - estado_iluminacion: 'Adecuada', 'Cercana al límite', 'Fuera de rango' o 'Sin monitoreo'
    - nivel_alerta: 'verde', 'amarillo' o 'rojo'
    - categoria: 'adecuado', 'insuficiente', 'excesivo' o 'sin_datos'
    """
    if lux is None:
        return {
            'estado_iluminacion': 'Sin monitoreo',
            'nivel_alerta': 'rojo',
            'categoria': 'sin_datos',
        }

    if lux_minimo is None or lux_maximo is None:
        if lux <= 100:
            return {
                'estado_iluminacion': 'Fuera de rango',
                'nivel_alerta': 'rojo',
                'categoria': 'insuficiente',
            }
        if lux <= 6000:
            return {
                'estado_iluminacion': 'Adecuada',
                'nivel_alerta': 'verde',
                'categoria': 'adecuado',
            }
        return {
            'estado_iluminacion': 'Fuera de rango',
            'nivel_alerta': 'rojo',
            'categoria': 'excesivo',
        }

    if lux < lux_minimo:
        return {
            'estado_iluminacion': 'Fuera de rango',
            'nivel_alerta': 'rojo',
            'categoria': 'insuficiente',
        }

    if lux > lux_maximo:
        return {
            'estado_iluminacion': 'Fuera de rango',
            'nivel_alerta': 'rojo',
            'categoria': 'excesivo',
        }

    rango = lux_maximo - lux_minimo
    margen = max(1.0, rango * 0.1)
    if lux - lux_minimo <= margen or lux_maximo - lux <= margen:
        return {
            'estado_iluminacion': 'Cercana al límite',
            'nivel_alerta': 'amarillo',
            'categoria': 'adecuado',
        }

    return {
        'estado_iluminacion': 'Adecuada',
        'nivel_alerta': 'verde',
        'categoria': 'adecuado',
    }
