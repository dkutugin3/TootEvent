from abc import ABC, abstractmethod


class AbstractBookingUseCase(ABC):

    @abstractmethod
    async def buy(self, event_id: int, number_of_tickets: int, user_id: int): ...

    @abstractmethod
    async def get_info(self, booking_id: int, user_id: int): ...

    @abstractmethod
    async def get_list_by_current_user(self, user_id: int): ...

    @abstractmethod
    async def get_list_by_user(self, target_user_id: int, user_id: int): ...

    @abstractmethod
    async def get_list_by_event(self, event_id: int, user_id: int): ...

    @abstractmethod
    async def get_list(self, user_id: int): ...

    @abstractmethod
    async def delete(self, booking_id: int, user_id: int): ...
