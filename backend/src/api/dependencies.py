from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from config import settings
from schemas.exceptions import (
    IncorrectTokenFormatExcepetion,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from repositories.users import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatExcepetion
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
