from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.tickets import TicketSchema


class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)

    def to_read_model(self) -> TicketSchema:
        return TicketSchema(
            id=self.id,
            booking_id=self.booking_id
        )
