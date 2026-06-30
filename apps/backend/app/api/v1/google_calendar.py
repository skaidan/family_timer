from fastapi import APIRouter, Body, HTTPException, Query

from ...integrations.google_calendar import GoogleCalendarClient

router = APIRouter(prefix="/google-calendar", tags=["google-calendar"])


@router.get("/auth-url")
def get_auth_url() -> dict[str, str]:
    client = GoogleCalendarClient()
    auth_url = client.get_auth_url()
    if not auth_url:
        raise HTTPException(
            status_code=503,
            detail="Google Calendar no está configurado. Define GOOGLE_CLIENT_ID y GOOGLE_REDIRECT_URI.",
        )
    return {"auth_url": auth_url}


@router.post("/token")
def exchange_token(code: str = Body(..., embed=True)) -> dict[str, object]:
    client = GoogleCalendarClient()
    if not client.client_id or not client.client_secret or not client.redirect_uri:
        raise HTTPException(
            status_code=503,
            detail="Google Calendar no está configurado. Define GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET y GOOGLE_REDIRECT_URI.",
        )
    try:
        token_data = client.exchange_code(code)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return token_data


@router.get("/events")
def get_events(access_token: str = Query(...)) -> dict[str, object]:
    client = GoogleCalendarClient()
    try:
        events = client.fetch_events(access_token)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"events": events}
