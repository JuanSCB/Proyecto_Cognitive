import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from app import create_app, db
from app.decorators import create_token
from app.models import Actividad, Salon, Sensor, HistorialIluminacion

app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})

with app.app_context():
    db.create_all()
    actividad = Actividad(nombre='Clase prueba', descripcion='Descripcion')
    db.session.add(actividad)
    db.session.commit()

    salon = Salon(
        nombre='Aula IA 101',
        ubicacion='Edificio D',
        descripcion='Sala de análisis',
        actividad_id=actividad.id
    )
    db.session.add(salon)
    db.session.commit()

    sensor = Sensor(
        salon_id=salon.id,
        lux=140.0,
        intensidad_led=65,
        consumo_energetico=1.1,
        modo_automatico=True
    )
    db.session.add(sensor)
    db.session.commit()

    db.session.add_all([
        HistorialIluminacion(sensor_id=sensor.id, lux=130.0, intensidad_led=60, consumo_energetico=1.0, modo_automatico=True),
        HistorialIluminacion(sensor_id=sensor.id, lux=150.0, intensidad_led=70, consumo_energetico=1.2, modo_automatico=True),
    ])
    db.session.commit()

    token = create_token(user_id=1, role='alumno')
    client = app.test_client()

    try:
        resp = client.post(
            f'/api/ai/analyze-room/{salon.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        print('status', resp.status_code)
        print('data', resp.get_data(as_text=True))
        print('json', resp.get_json(silent=True))
    except Exception:
        import traceback
        traceback.print_exc()
