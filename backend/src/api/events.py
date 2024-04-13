from fastapi import APIRouter, Response, Depends

from schemas.events import EventInfoSchema, EventAddSchema
from utils.dependencies import UOWDep
from services.events import EventsService

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/")
async def get_events_list(uow: UOWDep):
    return await EventsService.get_events_list(uow)


@router.post("/")
async def add_event(
    uow: UOWDep,
    event_data: EventAddSchema,
):
    await EventsService.add_event(uow, event_data,)
    return {"status": "ok"}


@router.get("/{event_id}")
async def get_event_info(
        uow: UOWDep, event_id: int) -> EventInfoSchema:
    return await EventsService.get_event_info(uow, event_id)


@router.delete("/{event_id}")
async def delete_event(
        uow: UOWDep, event_id: int):
    await EventsService.delete_event(uow, event_id)
    return {"status": "ok"}


@router.patch("/{event_id}")
async def change_event_info(
        uow: UOWDep, event_id: int, data: dict):
    await EventsService.change_event_info(uow, event_id, data)
    return {"status": "ok"}
