from pydantic import BaseModel, Field


class CheckSchema(BaseModel):
    id: int
    user_id: int
    events: list | None
    date: str
    total: int
    is_payed: bool


class CheckInfoSchema(BaseModel):
    id: int
    user_id: int
    events: list | None
    date: str
    total: int
    is_payed: bool
    is_expired: bool


class CheckAddSchema(BaseModel):
    events: list | None = Field(
        examples=[
            [
                {"id": 1, "tickets": 0},
            ]
        ]
    )
