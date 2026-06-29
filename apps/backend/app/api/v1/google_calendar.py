from fastapi import APIRouter, Query

from app.integrations.google_calendar import GoogleCalendarClient

router = APIRouter(prefix="/google-calendar", tags=["google-calendar"])
client = GoogleCalendarClient()


@router.get("/auth-url")
def get_auth_url() -> dict[str, str]:
    return {"auth_url": client.get_auth_url()}


@router.get("/events")
def get_events(access_token: str = Query(...)) -> dict[str, object]:
    events = client.fetch_events(access_token)
    return {"events": events}
