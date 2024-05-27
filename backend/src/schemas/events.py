from pydantic import BaseModel, Field


class EventSchema(BaseModel):
    id: int
    title: str = Field(max_length=30)
    date: str
    price: int
    genre: list | None
    places_left: int
    rating: int
    city: str
    place: str


class EventInfoSchema(BaseModel):
    title: str = Field(max_length=30)
    date: str
    price: int
    genre: list | None
    places_left: int
    rating: int
    city: str
    place: str


class EventAddSchema(BaseModel):
    title: str = Field(max_length=30, examples=["NineEleven"],)
    date: str = Field(
        examples=["11.09.2001 09:11", "DD.MM.YYYY HH:MM"]
    )
    price: int
    genre: list | None = Field(examples=[["comedy", "tradegy"], ["drama"]])
    total_places: int
    rating: int
    city: str = Field(examples=["New-York"])
    place: str = Field(examples=["Twin Towers"])
