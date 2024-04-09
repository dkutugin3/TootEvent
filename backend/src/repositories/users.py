from repositories.base import BaseDAO
from models.users import Users


class UsersDAO(BaseDAO):
    model = Users
