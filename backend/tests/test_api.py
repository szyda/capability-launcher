from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_list_capabilities():
    response = client.get('/api/capabilities')
    assert response.status_code == 200
    data = response.json()
    assert 'capabilities' in data
    assert len(data['capabilities']) >= 3


def test_get_known_capability():
    response = client.get('/api/capabilities/url_inspector')
    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == 'url_inspector'


def test_get_missing_capability_returns_404():
    response = client.get('/api/capabilities/does_not_exist')
    assert response.status_code == 404
    payload = response.json()
    assert payload['detail']['error'] == 'Capability not found'


def test_url_inspector_run():
    response = client.post('/api/capabilities/url_inspector/run', json={'inputs': {'url': 'https://example.com/path?x=1&y=2'}})
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'success'
    assert payload['result']['host'] == 'example.com'


def test_timezone_converter_run():
    response = client.post(
        '/api/capabilities/timezone_converter/run',
        json={'inputs': {'timestamp': '2026-11-12T09:30:00Z', 'from_tz': 'UTC', 'to_tz': 'Europe/London'}},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'success'
    assert 'converted_time' in payload['result']


def test_csv_cleaner_run():
    csv_value = 'name,age\nAda,36\n,\nLinus,54\nAda,36'
    response = client.post('/api/capabilities/csv_cleaner/run', json={'inputs': {'csv': csv_value}})
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'success'
    assert payload['result']['rows'] == 2


def test_invalid_input_rejected():
    response = client.post('/api/capabilities/url_inspector/run', json={'inputs': {'url': 123}})
    assert response.status_code == 422
    payload = response.json()
    assert payload['detail']['error'] == 'Invalid inputs'


def test_missing_required_input_rejected():
    response = client.post('/api/capabilities/url_inspector/run', json={'inputs': {}})
    assert response.status_code == 422


def test_unknown_route_is_404():
    response = client.get('/api/nope')
    assert response.status_code == 404


def test_run_unknown_capability_returns_404():
    response = client.post('/api/capabilities/ghost/run', json={'inputs': {'url': 'https://example.com'}})
    assert response.status_code == 404
    payload = response.json()
    assert payload['detail']['error'] == 'Capability not found'


def test_run_with_malformed_json_payload_is_422():
    response = client.post('/api/capabilities/url_inspector/run', data='not-json')
    assert response.status_code == 422
