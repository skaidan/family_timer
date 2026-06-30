import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app


client = TestClient(app)


def test_get_auth_url_returns_string():
    response = client.get('/google-calendar/auth-url')

    assert response.status_code == 200
    assert isinstance(response.json().get('auth_url'), str)


def test_get_events_requires_access_token():
    response = client.get('/google-calendar/events')

    assert response.status_code == 422


def test_get_timeline_without_token():
    response = client.get('/timeline')

    assert response.status_code == 200
    assert 'members' in response.json()
