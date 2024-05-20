from pydantic import BaseModel


class BookingSchema(BaseModel):
    id: int
    check_id: int
    user_id: int
    event_id: int
    number_of_tickets: int
    cost: int
    is_expired: bool


class BookingInfoSchema(BaseModel):
    check_id: int
    user_id: int
    event_id: int
    number_of_tickets: int
    cost: int
    is_expired: bool
