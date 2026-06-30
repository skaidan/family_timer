import os
from unittest.mock import MagicMock

import pytest

from apps.backend.app.integrations.google_calendar import GoogleCalendarClient


@pytest.fixture(autouse=True)
def clear_google_env(monkeypatch):
    monkeypatch.delenv('GOOGLE_CLIENT_ID', raising=False)
    monkeypatch.delenv('GOOGLE_CLIENT_SECRET', raising=False)
    monkeypatch.delenv('GOOGLE_REDIRECT_URI', raising=False)
    monkeypatch.delenv('GOOGLE_SCOPES', raising=False)


def test_get_auth_url_returns_empty_when_not_configured():
    client = GoogleCalendarClient()

    assert client.get_auth_url() == ''


def test_get_auth_url_includes_required_query_parameters(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID', 'test-client-id')
    monkeypatch.setenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080')
    monkeypatch.setenv('GOOGLE_SCOPES', 'https://www.googleapis.com/auth/calendar.readonly')

    client = GoogleCalendarClient()
    auth_url = client.get_auth_url()

    assert 'client_id=test-client-id' in auth_url
    assert 'redirect_uri=http%3A%2F%2Flocalhost%3A8080' in auth_url
    assert 'response_type=code' in auth_url
    assert 'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly' in auth_url


def test_parse_time_datetime():
    client = GoogleCalendarClient()
    result = client._parse_time({'dateTime': '2026-06-30T09:30:00Z'})

    assert result == 9.5


def test_parse_time_date_only():
    client = GoogleCalendarClient()
    result = client._parse_time({'date': '2026-06-30'})

    assert result == 0


def test_parse_event_daily_all_day():
    client = GoogleCalendarClient()
    event = {
        'summary': 'Fiesta',
        'start': {'date': '2026-06-30'},
        'end': {'date': '2026-07-01'},
    }

    parsed = client._parse_event(event)

    assert parsed is not None
    assert parsed['start'] == 0
    assert parsed['end'] == 24.0
    assert parsed['label'] == 'Fiesta'
    assert parsed['source'] == 'google_calendar'


def test_fetch_events_uses_httpx_get(monkeypatch):
    monkeypatch.setenv('GOOGLE_CLIENT_ID', 'test-client-id')
    monkeypatch.setenv('GOOGLE_CLIENT_SECRET', 'test-client-secret')
    monkeypatch.setenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080')

    expected = {
        'items': [
            {
                'summary': 'Prueba',
                'start': {'dateTime': '2026-06-30T08:00:00Z'},
                'end': {'dateTime': '2026-06-30T10:00:00Z'},
            }
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = expected
    mock_response.raise_for_status.return_value = None

    captured = {
        'headers': None,
        'params': None,
        'url': None,
    }

    def fake_get(url, headers=None, params=None, timeout=None):
        captured['url'] = url
        captured['headers'] = headers
        captured['params'] = params
        captured['timeout'] = timeout
        return mock_response

    monkeypatch.setattr('apps.backend.app.integrations.google_calendar.httpx.get', fake_get)

    client = GoogleCalendarClient()
    events = client.fetch_events('token-123')

    assert captured['url'].endswith('/calendar/v3/calendars/primary/events')
    assert captured['headers']['Authorization'] == 'Bearer token-123'
    assert isinstance(events, list)
    assert events[0]['summary'] == 'Prueba'
