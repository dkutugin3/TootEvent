from typing import List

from pydantic import BaseModel

from domain.usecases.tickets import AbstractTicketUseCase
from schemas.bookings import BookingInfoSchema
from schemas.exceptions import AccessForbiddenException, RefundDeclinedException
from services.bookings import BookingsService
from services.events import EventsService
from services.tickets import TicketsService
from services.users import UsersService
from utils.dependencies import UOWDep

from utils.date_manager import DateManager as Dm
from itertools import chain


class TicketUseCase(AbstractTicketUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def get_list_by_current_user(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            bookings = await BookingsService.get_bookings_list(self.uow, user_id=user_id)
            tickets_list = []
            for booking in bookings:
                tickets_list = list(
                    chain(tickets_list, await TicketsService.get_tickets_list(self.uow, booking_id=booking.id)))

        return tickets_list

    async def get_list(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            tickets_list = await TicketsService.get_tickets_list(self.uow)

        return tickets_list

    async def get_list_by_user(self, target_user_id: int, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException

            bookings = await BookingsService.get_bookings_list(self.uow, user_id=target_user_id)
            tickets_list = []
            for booking in bookings:
                tickets_list = list(
                    chain(tickets_list, await TicketsService.get_tickets_list(self.uow, booking_id=booking.id)))

        return tickets_list

    async def get_info(self, ticket_id: int, user_id: int) -> BookingInfoSchema:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            booking = await TicketsService.get_ticket_info(self.uow, ticket_id)

        return booking

    async def refund(
            self,
            ticket_id: int,
            user_id: int
    ):
        date = Dm.now()
        async with self.uow:
            booking = await TicketsService.get_ticket_info(self.uow, ticket_id)
            if booking.user_id != user_id:
                raise AccessForbiddenException

            event_date = Dm.string_to_date((await EventsService.get_event_info(self.uow, booking.event_id)).date)
            if date > Dm.add(event_date, days=-2):
                raise RefundDeclinedException

            # payment logic

            await TicketsService.delete_ticket_by_id(self.uow, ticket_id)
            if booking.number_of_tickets > 1:
                await BookingsService.update_booking_info(self.uow, booking.id,
                                                          number_of_tickets=booking.number_of_tickets - 1)
            else:
                await BookingsService.delete_booking_by_id(self.uow, booking.id)

            await self.uow.commit()

    async def delete(
            self,
            ticket_id: int,
            user_id: int
    ):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            booking = await TicketsService.get_ticket_info(self.uow, ticket_id)
            await TicketsService.delete_ticket_by_id(self.uow, ticket_id)

            if booking.number_of_tickets > 1:
                await BookingsService.update_booking_info(self.uow, booking.id,
                                                          number_of_tickets=booking.number_of_tickets - 1)
            else:
                await BookingsService.delete_booking_by_id(self.uow, booking.id)

            await self.uow.commit()
