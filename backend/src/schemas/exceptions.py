from fastapi import HTTPException, status


class BException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class UnauthorizedException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не авторизован"


class IncorrectEmailOrPasswordException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatExcepetion(BException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BException):
    status_code = status.HTTP_401_UNAUTHORIZED