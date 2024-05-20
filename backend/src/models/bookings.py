from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.bookings import BookingSchema


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    number_of_tickets: Mapped[int] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    is_expired: Mapped[bool] = mapped_column(default=False, nullable=False)

    def to_read_model(self) -> BookingSchema:
        return BookingSchema(
            id=self.id,
            check_id=self.check_id,
            user_id=self.user_id,
            event_id=self.event_id,
            number_of_tickets=self.number_of_tickets,
            cost=self.cost,
            is_expired=self.is_expired
        )
