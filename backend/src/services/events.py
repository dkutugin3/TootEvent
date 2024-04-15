from fastapi import Response, Depends
from pydantic import BaseModel

from schemas.events import EventSchema, EventAddSchema, EventInfoSchema
from utils.unit_of_work import AbstractUOW

from typing import List

from utils.date_manager import DateManager as Dm


class EventsService:
    @staticmethod
    async def add_event(
        uow: AbstractUOW, event: EventAddSchema,
    ) -> int:
        async with uow:
            event_id = await uow.events.add_one(
                title=event.title,
                date=Dm.string_to_date(event.date),
                price=event.price,
                genre=event.genre,
                rating=event.rating,
                location=event.location,
            )
            await uow.commit()
            return event_id

    @staticmethod
    async  def get_events_list(uow: AbstractUOW) -> List[BaseModel]:
        async with uow:
            events = await uow.events.find_all()
            return events

    @staticmethod
    async def get_event_info(uow: AbstractUOW, event_id: int) -> EventInfoSchema:
        async with uow:
            event = await uow.events.find_one(id=event_id)

            return EventInfoSchema(**event.dict())

    @staticmethod
    async def change_event_info(
            uow: AbstractUOW, event_id: int, data: dict,
    ):
        async with uow:
            await uow.events.update_by_id(event_id, **data)
            await uow.commit()

    @staticmethod
    async  def delete_event(uow: AbstractUOW, event_id: int):
        async with uow:
            await uow.events.delete_by_id(model_id=event_id)
            await uow.commit()
