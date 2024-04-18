from fastapi import APIRouter, Response, Depends

from schemas.events import EventInfoSchema, EventAddSchema
from schemas.exceptions import AccessForbiddenException
from usecases.dependencies import EventCase
from utils.dependencies import UOWDep

from usecases.event import EventUseCase
from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/")
async def get_events_list(event_case: EventCase):
    return await event_case.get_list()


@router.get("/{event_id}")
async def get_event_info(event_id: int, event_case: EventCase) -> EventInfoSchema:
    return await event_case.get_info(event_id)


@router.post("/")
async def add_event(
    event_data: EventAddSchema,
    event_case: EventCase,
    user_id: int = Depends(get_current_user_id),
):
    await event_case.add(event_data, user_id)
    return {"status": "ok"}


@router.delete("/{event_id}")
async def delete_event(
    event_id: int, event_case: EventCase, user_id: int = Depends(get_current_user_id)
):
    await event_case.delete(event_id, user_id)
    return {"status": "ok"}


@router.patch("/{event_id}")
async def change_event_info(
    event_id: int,
    data: dict,
    event_case: EventCase,
    user_id: int = Depends(get_current_user_id),
):

    await event_case.update(event_id, user_id, **data)
    return {"status": "ok"}
