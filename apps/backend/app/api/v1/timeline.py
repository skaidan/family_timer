from fastapi import APIRouter

from app.services.timeline_service import TimelineService

router = APIRouter(prefix="/timeline", tags=["timeline"])
service = TimelineService()


@router.get("")
def get_timeline() -> dict[str, object]:
    return service.build_timeline_by_member()
