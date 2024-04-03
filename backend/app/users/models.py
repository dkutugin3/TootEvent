from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    hashed_password: Mapped[str]
    preferences: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
