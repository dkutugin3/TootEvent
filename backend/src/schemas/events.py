from typing import Annotated
from pydantic import BaseModel, StringConstraints, Field

import datetime as dt


class EventSchema(BaseModel):
    id: int
    title: str = Field(max_length=30)
    date: str
    price: int
    genre: list | None
    rating: int
    location: dict | None


class EventInfoSchema(BaseModel):
    title: str = Field(max_length=30)
    date: str
    price: int
    genre: list | None
    rating: int
    location: dict | None


class EventAddSchema(BaseModel):
    title: str = Field(max_length=30, examples=["NineEleven"])
    date: str = Field(examples=["11.09.2001 09:11 UTC +0300", "DD.MM.YYYY HH:MM UTC +HHMM"])
    price: int
    genre: list | None = Field(examples=[["comedy", "tradegy"], ["drama"]])
    rating: int
    location: dict | None = Field(examples=[{"country": "USA", "city": "NewYork"}])