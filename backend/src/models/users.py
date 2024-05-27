from db.database import Base
from schemas.users import UserSchema
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    hashed_password: Mapped[str]
    preferences: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    is_moderator: Mapped[bool] = mapped_column(nullable=False, default=True)
    avatar_path: Mapped[str] = mapped_column(nullable=True)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            email=self.email,
            name=self.name,
            hashed_password=self.hashed_password,
            preferences=self.preferences,
            is_moderator=self.is_moderator,
            avatar_path=self.avatar_path,
        )
