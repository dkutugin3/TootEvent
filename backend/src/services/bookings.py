from pydantic import BaseModel

from schemas.bookings import BookingInfoSchema
from utils.unit_of_work import AbstractUOW

from typing import List

from utils.date_manager import DateManager as Dm


class BookingsService:
    @staticmethod
    async def add_booking(
            uow: AbstractUOW,
            event_id: int,
            user_id: int,
            number_of_tickets: int,
            date: str,
    ) -> int:
        booking_id = await uow.bookings.add_one(
            user_id=user_id,
            event_id=event_id,
            number_of_tickets=number_of_tickets,
            date=Dm.string_to_date(date)
        )
        return booking_id

    @staticmethod
    async def get_bookings_list(uow: AbstractUOW, **filter_by) -> List[BaseModel]:
        bookings = await uow.bookings.find_all(**filter_by)
        return bookings

    @staticmethod
    async def get_booking_info(uow: AbstractUOW, booking_id: int) -> BookingInfoSchema:
        booking = await uow.bookings.find_one(id=booking_id)
        return BookingInfoSchema(**booking.dict())

    @staticmethod
    async def delete_booking_by_id(uow: AbstractUOW, booking_id: int):
        await uow.bookings.delete_by_id(model_id=booking_id)

    @staticmethod
    async def delete_booking_by_event(uow: AbstractUOW, event_id: int, user_id: int):
        await uow.bookings.delete_by_event(event_id=event_id, user_id=user_id)

    @staticmethod
    async def update_booking_info(uow: AbstractUOW, booking_id: int, **to_update):
        await uow.bookings.update_by_id(booking_id, **to_update)
