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


def test_timeline_endpoint_includes_google_events(monkeypatch):
    import datetime

    class DummyCalendarClient:
        def fetch_events(self, access_token: str):
            return [
                {
                    'summary': 'Trabajo Papá',
                    'start_dt': datetime.datetime(2026, 7, 1, 9, 0, tzinfo=datetime.timezone.utc),
                    'end_dt': datetime.datetime(2026, 7, 1, 10, 0, tzinfo=datetime.timezone.utc),
                    'description': 'Reunión importante',
                },
            ]

    from apps.backend.app.api.v1 import timeline as timeline_module
    from apps.backend.app import main as main_module

    monkeypatch.setattr(timeline_module.service, 'google_client', DummyCalendarClient())
    monkeypatch.setattr(main_module.service, 'google_client', DummyCalendarClient())

    response_timeline = client.get('/timeline', params={'google_access_token': 'dummy'})
    response_api_timeline = client.get('/api/timeline', params={'google_access_token': 'dummy'})

    assert response_timeline.status_code == 200
    assert response_api_timeline.status_code == 200

    for response in (response_timeline, response_api_timeline):
        members = response.json().get('members', [])
        papa = next((m for m in members if m['name'] == 'Papá'), None)
        assert papa is not None
        assert any(activity['label'] == 'Trabajo' for activity in papa['activities'])
