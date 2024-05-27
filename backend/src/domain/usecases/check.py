from abc import ABC, abstractmethod

from schemas.checks import CheckAddSchema


class AbstractCheckUseCase(ABC):
    @abstractmethod
    async def create(self, user_id: int, data: CheckAddSchema): ...

    @abstractmethod
    async def commit_payment(self, check_id: int, user_id: int, card: int, cvv: int): ...

    @abstractmethod
    async def get_list_by_user(self, user_id: int, target_user_id: int, **filter_by): ...

    @abstractmethod
    async def get_list_by_current_user(self, user_id: int, **filter_by): ...
