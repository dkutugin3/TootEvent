from sqlalchemy import String, JSON
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from schemas.events import EventSchema
from db.database import Base

from utils.date_manager import DateManager as Dm


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    date = mapped_column(DateTime(timezone=False), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    genre: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)

    def to_read_model(self) -> EventSchema:
        return EventSchema(
            id=self.id,
            title=self.title,
            date=Dm.date_to_string(self.date),
            price=self.price,
            genre=self.genre,
            rating=self.rating,
            location=self.location,
        )
