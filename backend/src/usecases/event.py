from typing import List

from pydantic import BaseModel

from domain.usecases.event import AbstractEventUseCase
from schemas.events import EventAddSchema, EventInfoSchema
from schemas.exceptions import AccessForbiddenException
from services.bookings import BookingsService
from utils.dependencies import UOWDep
from services.events import EventsService
from services.users import UsersService


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

    async def add(self,
                  event: EventAddSchema,
                  user_id: int,
                  ) -> int:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            event_id = await EventsService.add_event(self.uow, event)

            await self.uow.commit()
        return event_id

    async def delete(self,
                     event_id: int,
                     user_id: int
                     ):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await EventsService.delete_event(self.uow, event_id)

            await self.uow.commit()

    async def edit_info(self,
                        event_id: int,
                        user_id: int,
                        **data
                        ):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await EventsService.change_event_info(self.uow, event_id, **data)

            await self.uow.commit()
