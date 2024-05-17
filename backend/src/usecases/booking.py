import datetime
from typing import List

from pydantic import BaseModel

from domain.usecases.booking import AbstractBookingUseCase
from schemas.bookings import BookingInfoSchema
from schemas.exceptions import AccessForbiddenException, EventAlreadyStartedException, BadRequestException, \
    RefundDeclinedException, PaymentExpiredException
from schemas.payment import RefundSchema, PaymentSchema
from services.events import EventsService
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

    async def add(
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

            booking_id = await BookingsService.add_booking(self.uow, event_id, user_id, number_of_tickets,
                                                           Dm.date_to_string(date))

            await self.uow.commit()
        return booking_id

    async def confirm(self, booking_id: int, user_id: int, card: int, cvv: int):
        date = Dm.now()
        async with self.uow:
            booking = await BookingsService.get_booking_info(self.uow, booking_id)
            if user_id != booking.user_id:
                raise BadRequestException
            if booking.is_payed:
                raise BadRequestException
            if date > Dm.add(Dm.string_to_date(booking.date), minutes=30):
                raise PaymentExpiredException

            # event = await EventsService.get_event_info(self.uow, booking.event_id)
            # if event.capacity == 0:
            #   raise AllTicketsSoldException
            # await EventsService.change_event_info(self.uow, event.id,
            #                                       capacity=(event.capacity - booking.number_of_tickets))

            # recive pay from {card cvv} {event.price * booking.number_of_tickets}

            await BookingsService.update_booking_info(self.uow, booking_id, is_payed=True)

            await self.uow.commit()

    async def refund(
            self,
            booking_id: int,
            user_id: int,
            card: int
    ):
        date = Dm.now()
        async with self.uow:
            booking = await BookingsService.get_booking_info(self.uow, booking_id)
            if booking.user_id != user_id:
                raise AccessForbiddenException

            event_date = Dm.string_to_date((await EventsService.get_event_info(self.uow, booking.event_id)).date)
            if date > Dm.add(event_date, days=-2):
                raise RefundDeclinedException

            await BookingsService.update_booking_info(self.uow, booking_id, is_payed=False)
            # await BookingsService.delete_booking_by_id(self.uow, booking.id)

            # event = await EventsService.get_event_info(self.uow, booking.event_id)

            # await EventsService.change_event_info(self.uow, event.id, capacity=(event.capacity+1))

            # payment to {req.card} {event.price}

            await self.uow.commit()

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
