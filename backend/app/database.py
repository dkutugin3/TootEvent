from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Base = declarative_base()

class Base(DeclarativeBase):
    pass
