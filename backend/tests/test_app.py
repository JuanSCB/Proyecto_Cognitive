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
    sensor_payload = {
        'lux': 120.5,
        'intensidad_led': 80,
        'consumo_energetico': 1.2,
        'modo_automatico': True
    }
    response = test_client.post('/api/sensores', json=sensor_payload)
    assert response.status_code == 201
    result = response.get_json()
    assert result['lux'] == sensor_payload['lux']

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
    sensor_payload = {
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


def test_duplicate_activity_returns_conflict(test_client):
    payload = {'nombre': 'Iluminación sala', 'descripcion': 'Duplicado'}
    create_resp = test_client.post('/api/actividades', json=payload)
    assert create_resp.status_code == 201

    duplicate_resp = test_client.post('/api/actividades', json=payload)
    assert duplicate_resp.status_code == 409
    assert duplicate_resp.get_json()['error'] is True
