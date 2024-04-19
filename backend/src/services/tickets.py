from pydantic import BaseModel

from schemas.bookings import BookingInfoSchema
from utils.unit_of_work import AbstractUOW

from typing import List

from utils.date_manager import DateManager as Dm


class TicketsService:
    @staticmethod
    async def add_ticket(
            uow: AbstractUOW,
            booking_id: int
    ) -> int:
        ticket_id = await uow.tickets.add_one(
            booking_id=booking_id
        )
        return ticket_id

    @staticmethod
    async def get_tickets_list(uow: AbstractUOW, **filter_by) -> List[BaseModel]:
        tickets = await uow.tickets.find_all(**filter_by)
        return tickets

    @staticmethod
    async def get_ticket_info(uow: AbstractUOW, ticket_id: int):
        ticket = await uow.tickets.find_one(id=ticket_id)
        booking = await uow.bookings.find_one(id=ticket.booking_id)
        return booking

    @staticmethod
    async def delete_ticket_by_id(uow: AbstractUOW, ticket_id: int):
        await uow.tickets.delete_by_id(model_id=ticket_id)
