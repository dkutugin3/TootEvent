from models.events import Events
from repositories.alchemy import SqlAlchemyRepo
from sqlalchemy import update

from utils.date_manager import DateManager as Dm


class EventsRepo(SqlAlchemyRepo):
    model = Events

    async def update_by_id(self, model_id: int, **data):
        if data.get("date"):
            data["date"] = Dm.string_to_date(data["date"])
        stmt = update(self.model).where(self.model.id == model_id).values(**data)
        await self.session.execute(stmt)
