from abc import ABC, abstractmethod

from repositories.events import EventsRepo
from repositories.users import UsersRepo


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
