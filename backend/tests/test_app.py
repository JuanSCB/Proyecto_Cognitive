from app import db
from app.decorators import create_token
from app.models.historial_iluminacion import HistorialIluminacion
from app.services import ai_service


def test_get_configuracion(test_client):
    response = test_client.get('/docs')
    assert response.status_code == 200


def test_activity_crud_flow(test_client):
    payload = {'nombre': 'Iluminación sala', 'descripcion': 'Configuración para sala de reuniones'}
    create_resp = test_client.post('/api/actividades', json=payload)
    assert create_resp.status_code == 201
    data = create_resp.get_json()
    assert data['nombre'] == payload['nombre']

    id_ = data['id']
    update_resp = test_client.put(f'/api/actividades/{id_}', json={'nombre': 'Iluminación sala', 'descripcion': 'Ajuste actualizado'})
    assert update_resp.status_code == 200
    list_resp = test_client.get('/api/actividades')
    assert list_resp.status_code == 200
    assert any(item['id'] == id_ for item in list_resp.get_json())

    delete_resp = test_client.delete(f'/api/actividades/{id_}')
    assert delete_resp.status_code == 200


def test_sensor_registration_and_report(test_client):
    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula A101',
        'ubicacion': 'Edificio A, planta baja',
        'descripcion': 'Sala de reuniones principal'
    })
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    sensor_payload = {
        'salon_id': salon_id,
        'lux': 120.5,
        'intensidad_led': 80,
        'consumo_energetico': 1.2,
        'modo_automatico': True
    }
    response = test_client.post('/api/sensores', json=sensor_payload)
    assert response.status_code == 201
    result = response.get_json()
    assert result['lux'] == sensor_payload['lux']
    assert result['salon_id'] == salon_id

    report_resp = test_client.get('/api/reportes')
    assert report_resp.status_code == 200
    report_data = report_resp.get_json()
    assert 'total_registros' in report_data
    assert report_data['energia_total'] >= 0


def test_user_crud_flow(test_client):
    payload = {'nombre': 'Juan Pérez', 'correo': 'juan.perez@ejemplo.com'}
    create_resp = test_client.post('/api/usuarios', json=payload)
    assert create_resp.status_code == 201
    data = create_resp.get_json()
    assert data['nombre'] == payload['nombre']
    assert data['correo'] == payload['correo']

    user_id = data['id']
    get_resp = test_client.get(f'/api/usuarios/{user_id}')
    assert get_resp.status_code == 200
    assert get_resp.get_json()['correo'] == payload['correo']

    update_resp = test_client.put(f'/api/usuarios/{user_id}', json={'nombre': 'Juan P', 'correo': 'juan.p@ejemplo.com'})
    assert update_resp.status_code == 200
    assert update_resp.get_json()['nombre'] == 'Juan P'

    delete_resp = test_client.delete(f'/api/usuarios/{user_id}')
    assert delete_resp.status_code == 200


def test_historial_and_consumo_endpoints(test_client):
    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula B202',
        'ubicacion': 'Edificio B, segundo piso',
        'descripcion': 'Laboratorio de ciencias'
    })
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    sensor_payload = {
        'salon_id': salon_id,
        'lux': 80.0,
        'intensidad_led': 50,
        'consumo_energetico': 0.75,
        'modo_automatico': False
    }
    response = test_client.post('/api/sensores', json=sensor_payload)
    assert response.status_code == 201

    historial_resp = test_client.get('/api/historial')
    assert historial_resp.status_code == 200
    assert isinstance(historial_resp.get_json(), list)

    consumo_resp = test_client.get('/api/consumo')
    assert consumo_resp.status_code == 200
    assert isinstance(consumo_resp.get_json(), list)


def test_sensor_latest_and_metrics(test_client):
    response = test_client.get('/api/sensores/latest')
    assert response.status_code == 200
    latest = response.get_json()
    assert 'lux' in latest
    assert 'intensidad_led' in latest

    promedio_resp = test_client.get('/api/reportes/promedio-lux')
    assert promedio_resp.status_code == 200
    promedio = promedio_resp.get_json()
    assert 'promedio_lux' in promedio
    assert promedio['cantidad_registros'] >= 1

    total_resp = test_client.get('/api/reportes/consumo-total')
    assert total_resp.status_code == 200
    assert 'total_consumo' in total_resp.get_json()

    stats_resp = test_client.get('/api/reportes/estadisticas')
    assert stats_resp.status_code == 200
    stats = stats_resp.get_json()
    assert 'cantidad_registros' in stats
    assert 'ultimo_registro' in stats


def test_salon_crud_and_salon_sensors(test_client):
    payload = {
        'nombre': 'Aula C303',
        'ubicacion': 'Edificio C, tercer piso',
        'descripcion': 'Sala de proyecciones'
    }
    create_resp = test_client.post('/api/salones', json=payload)
    assert create_resp.status_code == 201
    salon = create_resp.get_json()
    salon_id = salon['id']

    get_resp = test_client.get(f'/api/salones/{salon_id}')
    assert get_resp.status_code == 200
    assert get_resp.get_json()['nombre'] == payload['nombre']

    update_resp = test_client.put(f'/api/salones/{salon_id}', json={'nombre': 'Aula C303 Actualizada'})
    assert update_resp.status_code == 200
    assert update_resp.get_json()['nombre'] == 'Aula C303 Actualizada'

    sensor_resp = test_client.post('/api/sensores', json={
        'salon_id': salon_id,
        'lux': 95.0,
        'intensidad_led': 55,
        'consumo_energetico': 0.95,
        'modo_automatico': True
    })
    assert sensor_resp.status_code == 201

    sensores_resp = test_client.get(f'/api/salones/{salon_id}/sensores')
    assert sensores_resp.status_code == 200
    sensors = sensores_resp.get_json()
    assert isinstance(sensors, list)
    assert any(item['salon_id'] == salon_id for item in sensors)

    delete_resp = test_client.delete(f'/api/salones/{salon_id}')
    assert delete_resp.status_code == 200


def test_chat_analysis_uses_real_room_data(test_client, monkeypatch):
    with test_client.application.app_context():
        professor_token = create_token(user_id=1, role='administrador')
        activity_resp = test_client.post('/api/actividades', json={'nombre': 'Clase de laboratorio', 'descripcion': 'Prueba', 'lux_minimo': 100, 'lux_maximo': 300}, headers={'Authorization': f'Bearer {professor_token}'})
        assert activity_resp.status_code == 201
        actividad_id = activity_resp.get_json()['id']

        salon_resp = test_client.post('/api/salones', json={
            'nombre': 'Laboratorio A',
            'ubicacion': 'Edificio A',
            'descripcion': 'Sala para análisis',
            'actividad_id': actividad_id
        }, headers={'Authorization': f'Bearer {professor_token}'})
        assert salon_resp.status_code == 201
        salon_id = salon_resp.get_json()['id']

        sensor_resp = test_client.post('/api/sensores', json={
            'salon_id': salon_id,
            'lux': 180.0,
            'intensidad_led': 72,
            'consumo_energetico': 1.4,
            'modo_automatico': True
        }, headers={'Authorization': f'Bearer {professor_token}'})
        assert sensor_resp.status_code == 201
        sensor_id = sensor_resp.get_json()['id']

        db.session.add_all([
            HistorialIluminacion(sensor_id=sensor_id, lux=160.0, intensidad_led=68, consumo_energetico=1.2, modo_automatico=True),
            HistorialIluminacion(sensor_id=sensor_id, lux=190.0, intensidad_led=74, consumo_energetico=1.5, modo_automatico=True),
        ])
        db.session.commit()

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {'response': 'Estado general estable con iluminación adecuada.'}

    monkeypatch.setattr('app.controllers.chat_controller.requests.post', lambda *args, **kwargs: FakeResponse())

    response = test_client.post('/api/chat', json={'mensaje': 'Analiza el Laboratorio A'})
    assert response.status_code == 200
    assert response.get_json()['respuesta'] == 'Estado general estable con iluminación adecuada.'


def test_ai_analysis_endpoint_uses_real_room_data(test_client, monkeypatch):
    with test_client.application.app_context():
        professor_token = create_token(user_id=1, role='administrador')
    activity_resp = test_client.post('/api/actividades', json={'nombre': 'Clase Teórica IA', 'descripcion': 'Análisis de prueba', 'lux_minimo': 100, 'lux_maximo': 200}, headers={'Authorization': f'Bearer {professor_token}'})
    assert activity_resp.status_code == 201
    actividad_id = activity_resp.get_json()['id']

    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula IA 101',
        'ubicacion': 'Edificio IA',
        'descripcion': 'Sala para análisis inteligente',
        'actividad_id': actividad_id
    }, headers={'Authorization': f'Bearer {professor_token}'})
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    sensor_resp = test_client.post('/api/sensores', json={
        'salon_id': salon_id,
        'lux': 140.0,
        'intensidad_led': 65,
        'consumo_energetico': 1.1,
        'modo_automatico': True
    })
    assert sensor_resp.status_code == 201
    sensor_id = sensor_resp.get_json()['id']

    with test_client.application.app_context():
        db.session.add_all([
            HistorialIluminacion(sensor_id=sensor_id, lux=130.0, intensidad_led=60, consumo_energetico=1.0, modo_automatico=True),
            HistorialIluminacion(sensor_id=sensor_id, lux=150.0, intensidad_led=70, consumo_energetico=1.2, modo_automatico=True),
        ])
        db.session.commit()

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {'response': 'Estado general estable con iluminación adecuada.'}

    monkeypatch.setattr(ai_service.requests, 'post', lambda *args, **kwargs: FakeResponse())

    token = create_token(user_id=1, role='alumno')
    response = test_client.post(f'/api/ai/analyze-room/{salon_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['salon'] == 'Aula IA 101'
    assert data['analisis'] == 'Estado general estable con iluminación adecuada.'
    assert data['modelo'] == 'gemma3:1b'


def test_salon_current_activity_support(test_client):
    activity_resp = test_client.post('/api/actividades', json={'nombre': 'Clase Teórica', 'descripcion': 'Sesión magistral'})
    assert activity_resp.status_code == 201
    actividad_id = activity_resp.get_json()['id']

    salon_payload = {
        'nombre': 'Aula A101',
        'ubicacion': 'Pabellon A',
        'descripcion': 'Aula de Ingeniería',
        'actividad_id': actividad_id
    }
    create_resp = test_client.post('/api/salones', json=salon_payload)
    assert create_resp.status_code == 201
    salon = create_resp.get_json()
    assert salon['actividad_id'] == actividad_id
    assert salon['actividad_nombre'] == 'Clase Teórica'

    list_resp = test_client.get('/api/salones')
    assert list_resp.status_code == 200
    salons = list_resp.get_json()
    assert any(item['actividad_id'] == actividad_id and item['actividad_nombre'] == 'Clase Teórica' for item in salons)

    get_resp = test_client.get(f'/api/salones/{salon["id"]}')
    assert get_resp.status_code == 200
    fetched = get_resp.get_json()
    assert fetched['actividad_id'] == actividad_id
    assert fetched['actividad_nombre'] == 'Clase Teórica'

    update_resp = test_client.put(f'/api/salones/{salon["id"]}', json={'actividad_id': None})
    assert update_resp.status_code == 200
    updated = update_resp.get_json()
    assert updated['actividad_id'] is None
    assert updated['actividad_nombre'] is None


def test_dashboard_salones_endpoint(test_client):
    activity_resp = test_client.post('/api/actividades', json={'nombre': 'Clase Teórica Dashboard', 'descripcion': 'Sesión magistral', 'lux_minimo': 100, 'lux_maximo': 200})
    assert activity_resp.status_code == 201
    actividad_id = activity_resp.get_json()['id']

    payload = {
        'nombre': 'Aula D404',
        'ubicacion': 'Edificio D, cuarto piso',
        'descripcion': 'Sala de estudio',
        'actividad_id': actividad_id
    }
    create_resp = test_client.post('/api/salones', json=payload)
    assert create_resp.status_code == 201
    salon_id = create_resp.get_json()['id']

    sensor_resp = test_client.post('/api/sensores', json={
        'salon_id': salon_id,
        'lux': 150.0,
        'intensidad_led': 70,
        'consumo_energetico': 1.4,
        'modo_automatico': False
    })
    assert sensor_resp.status_code == 201

    dashboard_resp = test_client.get('/api/dashboard/salones')
    assert dashboard_resp.status_code == 200
    dashboard = dashboard_resp.get_json()
    found = next((item for item in dashboard if item['salon_id'] == salon_id), None)
    assert found is not None
    assert found['actividad_id'] == actividad_id
    assert found['actividad_nombre'] == 'Clase Teórica Dashboard'
    assert found['lux_minimo'] == 100
    assert found['lux_maximo'] == 200
    assert found['estado_iluminacion'] == 'Adecuada'
    assert found['nivel_alerta'] == 'verde'


def test_duplicate_activity_returns_conflict(test_client):
    payload = {'nombre': 'Iluminación sala', 'descripcion': 'Duplicado'}
    create_resp = test_client.post('/api/actividades', json=payload)
    assert create_resp.status_code == 201

    duplicate_resp = test_client.post('/api/actividades', json=payload)
    assert duplicate_resp.status_code == 409
    assert duplicate_resp.get_json()['error'] is True

def test_cumplimiento_iluminacion_endpoint(test_client):
    activity_resp = test_client.post('/api/actividades', json={
        'nombre': 'Clase Práctica Cumplimiento',
        'descripcion': 'Actividad de prueba',
        'lux_minimo': 100,
        'lux_maximo': 200
    })
    assert activity_resp.status_code == 201
    actividad_id = activity_resp.get_json()['id']

    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula E505',
        'ubicacion': 'Edificio E, quinto piso',
        'descripcion': 'Sala de pruebas',
        'actividad_id': actividad_id
    })
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    sensor_resp = test_client.post('/api/sensores', json={
        'salon_id': salon_id,
        'lux': 120.0,
        'intensidad_led': 60,
        'consumo_energetico': 0.8,
        'modo_automatico': True
    })
    assert sensor_resp.status_code == 201
    sensor_id = sensor_resp.get_json()['id']

    with test_client.application.app_context():
        db.session.add_all([
            HistorialIluminacion(sensor_id=sensor_id, lux=90.0, intensidad_led=50, consumo_energetico=0.5, modo_automatico=True),
            HistorialIluminacion(sensor_id=sensor_id, lux=150.0, intensidad_led=60, consumo_energetico=0.8, modo_automatico=True),
            HistorialIluminacion(sensor_id=sensor_id, lux=210.0, intensidad_led=70, consumo_energetico=1.0, modo_automatico=True),
        ])
        db.session.commit()

    response = test_client.get(f'/api/reportes/cumplimiento-iluminacion/{salon_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['salon_id'] == salon_id
    assert data['porcentaje_adecuado'] == 50
    assert data['porcentaje_insuficiente'] == 25
    assert data['porcentaje_excesivo'] == 25

def test_salon_historial_endpoint(test_client):
    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula F606',
        'ubicacion': 'Edificio F, sexto piso',
        'descripcion': 'Sala para historial'
    })
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    for i in range(3):
        sensor_resp = test_client.post('/api/sensores', json={
            'salon_id': salon_id,
            'lux': 100.0 + i * 10,
            'intensidad_led': 60 + i,
            'consumo_energetico': 0.8 + i * 0.05,
            'modo_automatico': True
        })
        assert sensor_resp.status_code == 201

    response = test_client.get(f'/api/salones/{salon_id}/historial')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert 'fecha' in data[0]
        assert 'lux' in data[0]
        assert 'intensidad_led' in data[0]
        assert 'consumo_energetico' in data[0]


def test_historial_con_salon_filter(test_client):
    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula G707',
        'ubicacion': 'Edificio G, septimo piso',
        'descripcion': 'Sala para filtrado'
    })
    assert salon_resp.status_code == 201
    salon_id = salon_resp.get_json()['id']

    sensor_resp = test_client.post('/api/sensores', json={
        'salon_id': salon_id,
        'lux': 150.0,
        'intensidad_led': 70,
        'consumo_energetico': 0.9,
        'modo_automatico': True
    })
    assert sensor_resp.status_code == 201

    response = test_client.get(f'/api/historial?salon_id={salon_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_salones_list_for_selector(test_client):
    salon_resp = test_client.post('/api/salones', json={
        'nombre': 'Aula H808',
        'ubicacion': 'Edificio H, octavo piso',
        'descripcion': 'Sala para selector'
    })
    assert salon_resp.status_code == 201

    response = test_client.get('/api/salones')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert 'id' in data[0]
        assert 'nombre' in data[0]
