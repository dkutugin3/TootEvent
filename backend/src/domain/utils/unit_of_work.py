from abc import ABC, abstractmethod

from repositories.bookings import BookingsRepo
from repositories.events import EventsRepo
from repositories.tickets import TicketsRepo
from repositories.users import UsersRepo


class AbstractUOW(ABC):
    users: UsersRepo
    events: EventsRepo
    bookings: BookingsRepo
    tickets: TicketsRepo

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
