from typing import List

from domain.usecases.event import AbstractEventUseCase
from pydantic import BaseModel
from schemas.events import EventAddSchema, EventInfoSchema
from schemas.exceptions import AccessForbiddenException
from services.bookings import BookingsService
from services.events import EventsService
from services.users import UsersService
from utils.dependencies import UOWDep


class EventUseCase(AbstractEventUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def get_list(self) -> List[BaseModel]:
        async with self.uow:
            await BookingsService.mark_if_expired(self.uow)
            events_list = await EventsService.get_events_list(self.uow)
            await self.uow.commit()

        return events_list

    async def get_info(self, event_id: int) -> EventInfoSchema:
        async with self.uow:
            await BookingsService.mark_if_expired(self.uow, event_id=event_id)
            event = await EventsService.get_event_info(self.uow, event_id)
            await self.uow.commit()

        return event

    async def add(
        self,
        event: EventAddSchema,
        user_id: int,
    ) -> int:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            event_id = await EventsService.add_event(self.uow, event)

            await self.uow.commit()
        return event_id

    async def delete(self, event_id: int, user_id: int):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await EventsService.delete_event(self.uow, event_id)

            await self.uow.commit()

    async def edit_info(self, event_id: int, user_id: int, **data):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await EventsService.change_event_info(self.uow, event_id, **data)

            await self.uow.commit()

    async def find_event(self, query: str):
        parts = query.lower().split()
        found: List[BaseModel] = []
        async with self.uow:
            events = await EventsService.get_events_list(self.uow)
            for event in events:
                representation = await EventsService.repr(event)
                for part in parts:
                    if part in representation:
                        found.append(event)
                        break
        return found
