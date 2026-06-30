from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os

from .api.v1.google_calendar import router as google_calendar_router
from .api.v1.timeline import router as timeline_router
from .services.timeline_service import TimelineService

app = FastAPI(title="Family Timer API")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_calendar_router)
app.include_router(timeline_router)

service = TimelineService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/timeline")
def api_timeline(google_access_token: str | None = Query(None)) -> dict[str, object]:
    return service.build_timeline_by_member(google_access_token)
