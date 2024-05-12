from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.bookings import BookingSchema

from utils.date_manager import DateManager as Dm


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    number_of_tickets: Mapped[int] = mapped_column(nullable=False)
    date = mapped_column(DateTime(timezone=False), nullable=False)
    is_payed: Mapped[bool] = mapped_column(default=False, nullable=False)

    def to_read_model(self) -> BookingSchema:
        return BookingSchema(
            id=self.id,
            user_id=self.user_id,
            event_id=self.event_id,
            number_of_tickets=self.number_of_tickets,
            date=Dm.date_to_string(self.date),
            is_payed=self.is_payed
        )
