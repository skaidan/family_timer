import datetime
import pytest

from apps.backend.app.services.timeline_service import TimelineService


class DummyCalendarClient:
    def fetch_events(self, access_token: str):
        if access_token == "valid_token":
            return [
                {
                    "summary": "Cole Lucía",
                    "start_dt": datetime.datetime(2026, 7, 1, 8, 0, tzinfo=datetime.timezone.utc),
                    "end_dt": datetime.datetime(2026, 7, 1, 10, 0, tzinfo=datetime.timezone.utc),
                    "description": "Clase de Lucía",
                },
                {
                    "summary": "Trabajo Papá",
                    "start_dt": datetime.datetime(2026, 7, 1, 9, 0, tzinfo=datetime.timezone.utc),
                    "end_dt": datetime.datetime(2026, 7, 1, 11, 0, tzinfo=datetime.timezone.utc),
                    "description": "Reunión importante",
                },
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


def test_build_timeline_assigns_ungrouped_google_events_to_google_calendar(timeline_service):
    service = timeline_service
    timeline = service.build_timeline_by_member("valid_token")

    google_calendar_member = next((m for m in timeline["members"] if m["name"] == "Google Calendar"), None)
    assert google_calendar_member is None


class UngroupedDummyCalendarClient(DummyCalendarClient):
    def fetch_events(self, access_token: str):
        if access_token == "valid_token":
            return [
                {
                    "summary": "Evento general",
                    "start_dt": datetime.datetime(2026, 7, 1, 8, 0, tzinfo=datetime.timezone.utc),
                    "end_dt": datetime.datetime(2026, 7, 1, 9, 0, tzinfo=datetime.timezone.utc),
                    "description": "Sin asignar",
                },
            ]
        raise ValueError("Token inválido")


def test_build_timeline_with_ungrouped_google_event(monkeypatch):
    service = TimelineService()
    monkeypatch.setattr(service, "google_client", UngroupedDummyCalendarClient())

    timeline = service.build_timeline_by_member("valid_token")
    google_member = next((m for m in timeline["members"] if m["name"] == "Google Calendar"), None)

    assert google_member is not None
    assert any(activity["label"] == "Actividad" for activity in google_member["activities"])


def test_build_timeline_with_all_day_google_event(monkeypatch):
    service = TimelineService()
    monkeypatch.setattr(
        service,
        "google_client",
        DummyCalendarClient(),
    )

    service.google_client.fetch_events = lambda access_token: [
        {
            "summary": "Todo el día Lucía",
            "start_dt": datetime.datetime(2026, 7, 1, 0, 0, tzinfo=datetime.timezone.utc),
            "end_dt": datetime.datetime(2026, 7, 2, 0, 0, tzinfo=datetime.timezone.utc),
            "description": "Día completo",
        }
    ]

    timeline = service.build_timeline_by_member("valid_token")
    lucia = next(member for member in timeline["members"] if member["name"] == "Lucía")

    assert any(activity["start"] == 0.0 and activity["end"] == 24.0 for activity in lucia["activities"])


def test_build_timeline_ignores_invalid_google_event_payload(monkeypatch):
    service = TimelineService()
    monkeypatch.setattr(
        service,
        "google_client",
        DummyCalendarClient(),
    )

    service.google_client.fetch_events = lambda access_token: [
        {"summary": "Sin tiempo"},
    ]

    timeline = service.build_timeline_by_member("valid_token")
    assert all("start" in activity and activity["start"] is not None for member in timeline["members"] for activity in member["activities"])
