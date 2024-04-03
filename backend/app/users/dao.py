from app.base_dao.base_dao import BaseDAO
from .models import Users


class UsersDAO(BaseDAO):
    model = Users
