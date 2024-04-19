from abc import ABC, abstractmethod


class AbstractTicketUseCase(ABC):

    @abstractmethod
    async def get_info(self, ticket_id: int, user_id: int): ...

    @abstractmethod
    async def get_list_by_current_user(self, user_id: int): ...

    @abstractmethod
    async def get_list_by_user(self, target_user_id: int, user_id: int): ...

    @abstractmethod
    async def get_list(self, user_id: int): ...

    @abstractmethod
    async def refund(self, ticket_id: int, user_id: int): ...

    @abstractmethod
    async def delete(self, ticket_id: int, user_id: int): ...
