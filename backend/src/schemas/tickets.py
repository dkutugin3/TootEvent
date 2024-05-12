from pydantic import BaseModel


class TicketSchema(BaseModel):
    id: int
    booking_id: int
