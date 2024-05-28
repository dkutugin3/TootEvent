from typing import List

from pydantic import BaseModel
from schemas.bookings import BookingInfoSchema
from utils.date_manager import DateManager as Dm
from utils.unit_of_work import AbstractUOW


class BookingsService:
    @staticmethod
    async def add_booking(
        uow: AbstractUOW,
        event_id: int,
        user_id: int,
        check_id: int,
        number_of_tickets: int,
        cost: int,
    ) -> int:
        booking_id = await uow.bookings.add_one(
            check_id=check_id,
            user_id=user_id,
            event_id=event_id,
            number_of_tickets=number_of_tickets,
            cost=cost,
            is_valid=True,
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
    async def update_booking_info(uow: AbstractUOW, booking_id: int, **to_update):
        await uow.bookings.update_by_id(booking_id, **to_update)

    @staticmethod
    async def mark_if_expired(uow: AbstractUOW, **filter_by) -> bool:
        is_expired = False
        date = Dm.now()
        bookings = await uow.bookings.find_all(is_valid=True, **filter_by)
        for booking in bookings:
            check = await uow.checks.find_one(id=booking.check_id)
            if (Dm.add(date, minutes=-30) > Dm.string_to_date(check.date)) and (
                not check.is_payed
            ):
                is_expired = True
                await uow.bookings.update_by_id(booking.id, is_valid=False)
                event = await uow.events.find_one(id=booking.event_id)
                await uow.events.update_by_id(
                    booking.event_id,
                    places_left=(event.places_left + booking.number_of_tickets),
                )

        return False
