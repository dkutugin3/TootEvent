from abc import ABC, abstractmethod

from schemas.events import EventAddSchema


class AbstractEventUseCase(ABC):

    @abstractmethod
    async def add(self, event: EventAddSchema, user_id: int): ...

    @abstractmethod
    async def get_list(self): ...

    @abstractmethod
    async def get_info(self, event_id: int): ...

    @abstractmethod
    async def delete(self, event_id: int, user_id: int): ...

    @abstractmethod
    async def edit_info(self, event_id: int, user_id: int, **data): ...

    @abstractmethod
    async def find_event(self, query: str): ...
