from sqlalchemy import delete

from models.bookings import Bookings
from repositories.alchemy import SqlAlchemyRepo


class BookingsRepo(SqlAlchemyRepo):
    model = Bookings

    async def delete_by_event(self, event_id: int, user_id):
        stmt = delete(self.model).where(self.model.event_id == event_id and self.model.user_id == user_id)
        await self.session.execute(stmt)