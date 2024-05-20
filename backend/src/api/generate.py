from fastapi import APIRouter, Depends

from services.auth.dependencies import get_current_user_id
from services.generate import GigaChatManager
from usecases.dependencies import EventCase

router = APIRouter(
    prefix="/generate",
    tags=["Generate"],
)


@router.post("/add_events/")
async def add_event(
        event_case: EventCase,
        user_id: int = Depends(get_current_user_id),
):
    await GigaChatManager.fill_bd(event_case=event_case, user_id=user_id)
    return {"status": "ok"}
