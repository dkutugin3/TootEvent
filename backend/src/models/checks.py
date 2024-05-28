from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.checks import CheckSchema
from utils.date_manager import DateManager as Dm


class Checks(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    events: Mapped[list | None] = mapped_column(JSON, nullable=False)
    date = mapped_column(DateTime(timezone=False), nullable=False)
    total: Mapped[int] = mapped_column(nullable=False)
    is_payed: Mapped[bool] = mapped_column(default=False, nullable=False)

    def to_read_model(self) -> CheckSchema:
        return CheckSchema(
            id=self.id,
            user_id=self.user_id,
            events=self.events,
            date=Dm.date_to_string(self.date),
            total=self.total,
            is_payed=self.is_payed,
        )
