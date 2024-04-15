from fastapi import Response, Depends
from pydantic import BaseModel

from schemas.events import EventSchema, EventAddSchema, EventInfoSchema
from utils.unit_of_work import AbstractUOW

from typing import List

from utils.date_manager import DateManager as Dm


class EventsService:
    @staticmethod
    async def add_event(
        uow: AbstractUOW,
        event: EventAddSchema,
    ) -> int:
        event_id = await uow.events.add_one(
            title=event.title,
            date=Dm.string_to_date(event.date),
            price=event.price,
            genre=event.genre,
            rating=event.rating,
            location=event.location,
        )
        return event_id

    @staticmethod
    async def get_events_list(uow: AbstractUOW) -> List[BaseModel]:
        events = await uow.events.find_all()
        return events

    @staticmethod
    async def get_event_info(uow: AbstractUOW, event_id: int) -> EventInfoSchema:
        event = await uow.events.find_one(id=event_id)
        return EventInfoSchema(**event.dict())

    @staticmethod
    async def change_event_info(
        uow: AbstractUOW,
        event_id: int,
        **data,
    ):
        await uow.events.update_by_id(event_id, **data)

    @staticmethod
    async def delete_event(uow: AbstractUOW, event_id: int):
        await uow.events.delete_by_id(model_id=event_id)
