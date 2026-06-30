import os
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import quote, urlencode

import httpx


class GoogleCalendarClient:
    """Cliente base preparado para integrar con la API de Google Calendar."""

    def __init__(self) -> None:
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "")
        self.scopes = os.getenv("GOOGLE_SCOPES", "https://www.googleapis.com/auth/calendar.readonly").split(",")

    def get_auth_url(self) -> str:
        if not self.client_id or not self.redirect_uri:
            return ""

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "access_type": "offline",
            "scope": " ".join(self.scopes),
            "prompt": "consent",
        }
        return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params, quote_via=quote)

    def exchange_code(self, code: str) -> dict[str, Any]:
        token_url = "https://oauth2.googleapis.com/token"
        response = httpx.post(
            token_url,
            data={
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def fetch_events(self, access_token: str) -> list[dict[str, Any]]:
        if not access_token:
            return []

        now = datetime.now(timezone.utc)
        params = {
            "singleEvents": "true",
            "orderBy": "startTime",
            "timeMin": now.isoformat().replace("+00:00", "Z"),
            "timeMax": (now + timedelta(days=1)).isoformat().replace("+00:00", "Z"),
            "maxResults": 50,
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

        response = httpx.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        items = response.json().get("items", [])

        events: list[dict[str, Any]] = []
        for item in items:
            event = self._parse_event(item)
            if event:
                events.append(event)

        return events

    def _parse_event(self, raw_event: dict[str, Any]) -> dict[str, Any] | None:
        start_value = raw_event.get("start", {})
        end_value = raw_event.get("end", {})
        start = self._parse_time(start_value)
        end = self._parse_time(end_value)

        if start is None or end is None:
            return None

        if "date" in start_value and "date" in end_value and end <= start:
            start_date = datetime.fromisoformat(start_value["date"])
            end_date = datetime.fromisoformat(end_value["date"])
            if end_date > start_date:
                end = 24.0

        return {
            "summary": raw_event.get("summary", "Evento"),
            "label": raw_event.get("summary", "Evento"),
            "start": start,
            "end": end,
            "location": raw_event.get("location"),
            "description": raw_event.get("description"),
            "status": raw_event.get("status"),
            "source": "google_calendar",
        }

    def _parse_time(self, value: dict[str, Any]) -> float | None:
        date_time = value.get("dateTime") or value.get("date")
        if not isinstance(date_time, str):
            return None

        if date_time.endswith("Z"):
            date_time = date_time[:-1] + "+00:00"

        try:
            dt = datetime.fromisoformat(date_time)
        except ValueError:
            return None

        return dt.hour + dt.minute / 60 + dt.second / 3600
