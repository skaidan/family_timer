import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app


client = TestClient(app)


def test_google_auth_url_returns_503_when_env_not_set(monkeypatch):
    monkeypatch.delenv('GOOGLE_CLIENT_ID', raising=False)
    monkeypatch.delenv('GOOGLE_REDIRECT_URI', raising=False)
    response = client.get('/google-calendar/auth-url')

    assert response.status_code == 503
    assert 'Google Calendar no está configurado' in response.json()['detail']


def test_timeline_uses_google_access_token_parameter(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID', 'test-client-id')
    monkeypatch.setenv('GOOGLE_CLIENT_SECRET', 'test-client-secret')
    monkeypatch.setenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080')

    response = client.get('/timeline', params={'google_access_token': 'dummy'})

    assert response.status_code == 200
    assert 'members' in response.json()


def test_get_events_requires_access_token():
    response = client.get('/google-calendar/events')

    assert response.status_code == 422
