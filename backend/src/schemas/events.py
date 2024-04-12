from typing import Annotated
from pydantic import BaseModel, StringConstraints, Field

import datetime as dt


class EventSchema(BaseModel):
    id: int
    title: str = Field(max_length=30)
    date: dt.datetime
    price: int
    genre: list | None
    rating: int
    location: dict | None


class EventInfoSchema(BaseModel):
    title: str = Field(max_length=30)
    date: dt.datetime
    price: int
    genre: list | None
    rating: int
    location: dict | None


class EventAddSchema(BaseModel):
    title: str = Field(max_length=30)
    date: dt.datetime
    price: int
    genre: list | None
    rating: int
    location: dict | None
