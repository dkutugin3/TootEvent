import datetime
from typing import List

from domain.usecases.booking import AbstractBookingUseCase
from domain.utils.unit_of_work import AbstractUOW
from pydantic import BaseModel
from schemas.bookings import BookingInfoSchema
from schemas.exceptions import (AccessForbiddenException,
                                CheckIsNotPayedException,
                                NotValidBookingException,
                                RefundDeclinedException)
from services.bookings import BookingsService
from services.checks import ChecksService
from services.events import EventsService
from services.users import UsersService
from utils.date_manager import DateManager as Dm
from utils.dependencies import UOWDep


class BookingUseCase(AbstractBookingUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def refund(self, booking_id: int, user_id: int, card: int):
        date = Dm.now()
        async with self.uow:
            booking = await BookingsService.get_booking_info(self.uow, booking_id)
            if booking.user_id != user_id:
                raise AccessForbiddenException
            if not booking.is_valid:
                raise NotValidBookingException
            check = await ChecksService.get_check_info(self.uow, booking.check_id)

            if not check.is_payed:
                raise CheckIsNotPayedException

            event_date = Dm.string_to_date(
                (await EventsService.get_event_info(self.uow, booking.event_id)).date
            )
            if date > Dm.add(event_date, days=-2):
                raise RefundDeclinedException

            await BookingsService.update_booking_info(
                self.uow, booking_id, is_valid=False
            )
            await EventsService.change_number_of_places_left(
                self.uow, booking.event_id, booking.number_of_tickets
            )

            # payment to <card> <booking.cost * booking.number_of_tickets>

            await self.uow.commit()

    async def get_list_by_current_user(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            await BookingsService.mark_if_expired(self.uow, user_id=user_id)
            bookings_list = await BookingsService.get_bookings_list(
                self.uow, user_id=user_id
            )
            await self.uow.commit()

        return bookings_list

    async def get_list(self, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.mark_if_expired(self.uow)
            bookings_list = await BookingsService.get_bookings_list(self.uow)
            await self.uow.commit()

        return bookings_list

    async def get_list_by_user(
        self, target_user_id: int, user_id: int
    ) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.mark_if_expired(self.uow, user_id=target_user_id)
            bookings_list = await BookingsService.get_bookings_list(
                self.uow, user_id=target_user_id
            )
            await self.uow.commit()

        return bookings_list

    async def get_list_by_event(self, event_id: int, user_id: int) -> List[BaseModel]:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.mark_if_expired(self.uow, event_id=event_id)
            bookings_list = await BookingsService.get_bookings_list(
                self.uow, event_id=event_id
            )
            await self.uow.commit()

        return bookings_list

    async def get_info(self, booking_id: int, user_id: int) -> BookingInfoSchema:
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.mark_if_expired(self.uow, booking_id=booking_id)
            booking = await BookingsService.get_booking_info(self.uow, booking_id)
            await self.uow.commit()

        return booking

    async def delete(self, booking_id: int, user_id: int):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            await BookingsService.mark_if_expired(self.uow, id=booking_id)
            await BookingsService.delete_booking_by_id(self.uow, booking_id)

            await self.uow.commit()
