import os
from typing import Any


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

        params = [
            f"client_id={self.client_id}",
            f"redirect_uri={self.redirect_uri}",
            "response_type=code",
            "access_type=offline",
            "scope=" + " ".join(self.scopes),
            "prompt=consent",
        ]
        return "https://accounts.google.com/o/oauth2/v2/auth?" + "&".join(params)

    def fetch_events(self, access_token: str) -> list[dict[str, Any]]:
        """Placeholder para la integración real con Google Calendar API."""
        return [
            {
                "summary": "Cole",
                "start": "2026-06-29T08:00:00",
                "end": "2026-06-29T12:00:00",
                "location": "Escuela",
            }
        ]
