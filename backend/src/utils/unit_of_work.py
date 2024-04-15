from abc import ABC, abstractmethod

from db.database import async_session_maker
from repositories.users import UsersRepo
from repositories.events import EventsRepo


class AbstractUOW(ABC):
    users: UsersRepo
    events: EventsRepo

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UOW(AbstractUOW):
    async def __aenter__(self):
        self.session = async_session_maker()
        self.users = UsersRepo(self.session)
        self.events = EventsRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
