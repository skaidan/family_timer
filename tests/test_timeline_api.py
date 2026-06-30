import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app


client = TestClient(app)


def test_timeline_endpoint_returns_members():
    response = client.get('/timeline')

    assert response.status_code == 200
    json_data = response.json()
    assert 'members' in json_data
    assert isinstance(json_data['members'], list)


def test_timeline_endpoint_accepts_google_token():
    response = client.get('/timeline', params={'google_access_token': 'dummy'})

    assert response.status_code == 200
    assert 'members' in response.json()
