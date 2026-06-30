from fastapi import APIRouter, Query

from app.services.timeline_service import TimelineService

router = APIRouter(prefix="/timeline", tags=["timeline"])
service = TimelineService()


@router.get("")
def get_timeline(google_access_token: str | None = Query(None)) -> dict[str, object]:
    return service.build_timeline_by_member(google_access_token)
