from sqlalchemy import delete

from models.tickets import Tickets
from repositories.alchemy import SqlAlchemyRepo


class TicketsRepo(SqlAlchemyRepo):
    model = Tickets
