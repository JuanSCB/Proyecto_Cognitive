from app import db
from app.models.user import Usuario
from app.models.activity import Actividad
from app.models.configuracion import Configuracion
from app.models.sensor import Sensor
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico

__all__ = [
    'db',
    'Usuario',
    'Actividad',
    'Configuracion',
    'Sensor',
    'HistorialIluminacion',
    'ConsumoEnergetico'
]
