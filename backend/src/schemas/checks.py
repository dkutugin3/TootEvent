from pydantic import BaseModel


class CheckSchema(BaseModel):
    id: int
    user_id: int
    events: dict | None
    date: str
    is_payed: bool


class CheckInfoSchema(BaseModel):
    user_id: int
    events: dict | None
    date: str
    is_payed: bool
