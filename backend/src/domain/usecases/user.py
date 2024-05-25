from abc import ABC, abstractmethod

from starlette.responses import Response

from schemas.auth import UserRegisterSchema, UserLoginSchema, UserInfoSchema


class AbstractUserUseCase(ABC):

    @abstractmethod
    async def registrate(self, user: UserRegisterSchema, response: Response): ...

    @abstractmethod
    async def login(self, user_data: UserLoginSchema, response: Response): ...

    @abstractmethod
    async def logout(self, response: Response): ...

    @abstractmethod
    async def get_info(self): ...

    @abstractmethod
    async def edit_info(self, user_id, target_user_id, **data): ...

    @abstractmethod
    async def edit_my_info(self, user_id, **data): ...
