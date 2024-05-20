from models.bookings import Bookings
from repositories.alchemy import SqlAlchemyRepo


class BookingsRepo(SqlAlchemyRepo):
    model = Bookings
