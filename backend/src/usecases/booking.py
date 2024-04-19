import datetime
from typing import List

from pydantic import BaseModel

from domain.usecases.booking import AbstractBookingUseCase
from schemas.bookings import BookingInfoSchema
from schemas.exceptions import AccessForbiddenException, EventAlreadyStartedException, BadRequestException, \
    RefundDeclinedException
from services.events import EventsService
from services.tickets import TicketsService
from utils.dependencies import UOWDep
from services.bookings import BookingsService
from services.users import UsersService

from utils.date_manager import DateManager as Dm


class BookingUseCase(AbstractBookingUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def get_list_by_current_user(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            bookings_list = await BookingsService.get_bookings_list(self.uow, user_id=user_id)

        return bookings_list

    async def get_list(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            bookings_list = await BookingsService.get_bookings_list(self.uow)

        return bookings_list

    async def get_list_by_user(self, target_user_id: int, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            bookings_list = await BookingsService.get_bookings_list(self.uow, user_id=target_user_id)

        return bookings_list

    async def get_list_by_event(self, event_id: int, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            bookings_list = await BookingsService.get_bookings_list(self.uow, event_id=event_id)

        return bookings_list

    async def get_info(self, booking_id: int, user_id: int) -> BookingInfoSchema:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            booking = await BookingsService.get_booking_info(self.uow, booking_id)

        return booking

    async def buy(
            self,
            event_id: int,
            number_of_tickets: int,
            user_id: int
    ) -> int:
        date = Dm.now()
        async with self.uow:
            event = await EventsService.get_event_info(self.uow, event_id)
            if date > Dm.add(Dm.string_to_date(event.date), hours=-1):
                raise EventAlreadyStartedException

            # if event.booked + number_of_tickets > event.capacity:
            #     raise AllTicketsSoldException

            # payment logic

            booking_id = await BookingsService.add_booking(self.uow, event_id, user_id, number_of_tickets,
                                                           Dm.date_to_string(date))

            # this must be called after payment confirmed
            for i in range(number_of_tickets):
                await TicketsService.add_ticket(self.uow, booking_id)

            await self.uow.commit()
        return booking_id

    async def delete(
            self,
            booking_id: int,
            user_id: int
    ):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.delete_booking_by_id(self.uow, booking_id)

            await self.uow.commit()
