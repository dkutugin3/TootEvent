from abc import ABC, abstractmethod

from repositories.bookings import BookingsRepo
from repositories.checks import ChecksRepo
from repositories.events import EventsRepo
from repositories.users import UsersRepo


class AbstractUOW(ABC):
    users: UsersRepo
    events: EventsRepo
    bookings: BookingsRepo
    checks: ChecksRepo

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
