from models.checks import Checks
from repositories.alchemy import SqlAlchemyRepo


class ChecksRepo(SqlAlchemyRepo):
    model = Checks
