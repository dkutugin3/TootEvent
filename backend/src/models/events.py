import pathlib

from db.database import Base
from schemas.events import EventSchema
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime
from utils.date_manager import DateManager as Dm


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    date = mapped_column(DateTime(timezone=False), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    genre: Mapped[dict | list | None] = mapped_column(JSON, nullable=False)
    places_left: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    place: Mapped[str] = mapped_column(nullable=False)

    def to_read_model(self) -> EventSchema:
        return EventSchema(
            id=self.id,
            title=self.title,
            date=Dm.date_to_string(self.date),
            price=self.price,
            genre=self.genre,
            places_left=self.places_left,
            rating=self.rating,
            city=self.city,
            place=self.place
        )
