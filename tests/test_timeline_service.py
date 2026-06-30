import pytest

from apps.backend.app.api.v1.timeline import router
from apps.backend.app.services.timeline_service import TimelineService


class DummyCalendarClient:
    def fetch_events(self, access_token: str):
        if access_token == "valid_token":
            return [
                {"summary": "Cole Lucía", "start": 8.0, "end": 10.0, "description": "Clase de Lucía"},
                {"summary": "Trabajo Papá", "start": 9.0, "end": 11.0, "description": "Reunión importante"},
            ]
        raise ValueError("Token inválido")


@pytest.fixture
def timeline_service(monkeypatch):
    service = TimelineService()
    monkeypatch.setattr(service, "google_client", DummyCalendarClient())
    return service


def test_build_timeline_no_google_events(timeline_service):
    timeline = timeline_service.build_timeline_by_member()

    assert "members" in timeline
    assert any(member["name"] == "Mamá" for member in timeline["members"])
    assert all("activities" in member for member in timeline["members"])


def test_build_timeline_with_google_events(timeline_service):
    timeline = timeline_service.build_timeline_by_member("valid_token")

    lucia = next(member for member in timeline["members"] if member["name"] == "Lucía")
    papa = next(member for member in timeline["members"] if member["name"] == "Papá")

    assert any(activity["label"] == "Cole" for activity in lucia["activities"])
    assert any(activity["label"] == "Trabajo" for activity in papa["activities"])


def test_build_timeline_with_invalid_google_token(timeline_service):
    timeline = timeline_service.build_timeline_by_member("invalid_token")

    assert "Google Calendar" not in [member["name"] for member in timeline["members"]]
