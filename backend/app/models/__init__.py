from app import db
from app.models.user import Usuario
from app.models.activity import Actividad
from app.models.sensor import Sensor
from app.models.salon import Salon
from app.models.historial_iluminacion import HistorialIluminacion
from app.models.consumo_energetico import ConsumoEnergetico

__all__ = [
    'db',
    'Usuario',
    'Actividad',
    'Sensor',
    'Salon',
    'HistorialIluminacion',
    'ConsumoEnergetico'
]
