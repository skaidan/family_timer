from fastapi import APIRouter, Body, HTTPException, Query

from app.integrations.google_calendar import GoogleCalendarClient

router = APIRouter(prefix="/google-calendar", tags=["google-calendar"])
client = GoogleCalendarClient()


@router.get("/auth-url")
def get_auth_url() -> dict[str, str]:
    return {"auth_url": client.get_auth_url()}


@router.post("/token")
def exchange_token(code: str = Body(..., embed=True)) -> dict[str, object]:
    try:
        token_data = client.exchange_code(code)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return token_data


@router.get("/events")
def get_events(access_token: str = Query(...)) -> dict[str, object]:
    events = client.fetch_events(access_token)
    return {"events": events}
