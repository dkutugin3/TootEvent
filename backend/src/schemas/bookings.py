from pydantic import BaseModel


class BookingSchema(BaseModel):
    id: int
    user_id: int
    event_id: int
    number_of_tickets: int
    date: str
    is_payed: bool


class BookingInfoSchema(BaseModel):
    user_id: int
    event_id: int
    number_of_tickets: int
    date: str
    is_payed: bool
