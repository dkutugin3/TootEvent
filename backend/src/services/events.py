from fastapi import Response, Depends

from schemas.events import EventSchema, EventAddSchema, EventInfoSchema
from utils.unit_of_work import AbstractUOW


class EventsService:
    @classmethod
    async def add_event(
        cls, uow: AbstractUOW, event: EventAddSchema,
    ) -> int:
        async with uow:
            event_id = await uow.events.add_one(
                title=event.title,
                date=event.date,
                price=event.price,
                genre=event.genre,
                rating=event.rating,
                location=event.location,
            )
            await uow.commit()
            # cls.setup_access_token(event_id=event_id, response=response)
            return event_id

    @staticmethod
    async def get_event_info(uow: AbstractUOW, event_id: int) -> EventInfoSchema:
        async with uow:
            event = await uow.events.find_one(id=event_id)

            return EventInfoSchema(**event.dict())
