from models.events import Events
from repositories.alchemy import SqlAlchemyRepo


class EventsRepo(SqlAlchemyRepo):
    model = Events
