from abc import ABC, abstractmethod


class AbstractCheckUseCase(ABC):
    @abstractmethod
    async def create(self, user_id: int, events: dict): ...

    @abstractmethod
    async def confirm(self, check_id: int, user_id: int, card: int, cvv: int): ...
