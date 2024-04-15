from fastapi import APIRouter, Response, Depends

from schemas.events import EventInfoSchema, EventAddSchema
from schemas.exceptions import AccessForbiddenException
from utils.dependencies import UOWDep

from services.events import EventsService
from services.users import UsersService
from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/")
async def get_events_list(uow: UOWDep):
    return await EventsService.get_events_list(uow)


@router.get("/{event_id}")
async def get_event_info(
        uow: UOWDep, event_id: int) -> EventInfoSchema:
    return await EventsService.get_event_info(uow, event_id)


@router.post("/")
async def add_event(
        uow: UOWDep,
        event_data: EventAddSchema,
        user_id: int = Depends(get_current_user_id)
):
    if not await UsersService.user_is_moderator(uow, user_id):
        raise AccessForbiddenException
    await EventsService.add_event(uow, event_data)
    return {"status": "ok"}


@router.delete("/{event_id}")
async def delete_event(
        uow: UOWDep,
        event_id: int,
        user_id: int = Depends(get_current_user_id)
):
    if not await UsersService.user_is_moderator(uow, user_id):
        raise AccessForbiddenException
    await EventsService.delete_event(uow, event_id)
    return {"status": "ok"}


@router.patch("/{event_id}")
async def change_event_info(
        uow: UOWDep,
        event_id: int,
        data: dict,
        user_id: int = Depends(get_current_user_id)
):
    if not await UsersService.user_is_moderator(uow, user_id):
        raise AccessForbiddenException
    await EventsService.change_event_info(uow, event_id, data)
    return {"status": "ok"}
