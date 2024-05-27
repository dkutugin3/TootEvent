from db.database import async_session_maker
from domain.utils.unit_of_work import AbstractUOW
from repositories.bookings import BookingsRepo
from repositories.checks import ChecksRepo
from repositories.events import EventsRepo
from repositories.users import UsersRepo


class UOW(AbstractUOW):
    async def __aenter__(self):
        self.session = async_session_maker()
        self.users = UsersRepo(self.session)
        self.events = EventsRepo(self.session)
        self.bookings = BookingsRepo(self.session)
        self.checks = ChecksRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
