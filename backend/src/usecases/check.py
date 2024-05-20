from domain.usecases.check import AbstractCheckUseCase
from schemas.exceptions import AccessForbiddenException, EventAlreadyStartedException, \
    PaymentExpiredException, NotEnoughPlacesLeftException
from schemas.payment import PaymentSchema
from services.checks import ChecksService
from services.events import EventsService
from utils.dependencies import UOWDep
from services.bookings import BookingsService

from utils.date_manager import DateManager as Dm


class CheckUseCase(AbstractCheckUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def create(self, user_id: int, events: dict):
        date = Dm.now()
        async with self.uow:
            check_id = await ChecksService.add_check(self.uow, user_id, events, Dm.date_to_string(date))
            for (event_id, number_of_tickets) in events.items():
                event_id = int(event_id)
                event = await EventsService.get_event_info(self.uow, event_id)

                if event.places_left < number_of_tickets:
                    raise NotEnoughPlacesLeftException
                if Dm.add(date, hours=2) > Dm.string_to_date(event.date):
                    raise EventAlreadyStartedException

                await EventsService.change_number_of_places_left(self.uow, event_id, -number_of_tickets)
                await BookingsService.add_booking(self.uow, event_id, user_id, check_id, number_of_tickets, event.price)

            await self.uow.commit()

    async def confirm(self, check_id: int, user_id: int, card: int, cvv: int):
        date = Dm.now()
        async with self.uow:
            check = await ChecksService.get_check_info(self.uow, check_id)

            if user_id != check.user_id:
                raise AccessForbiddenException

            is_expired = await BookingsService.mark_if_expired(self.uow, check_id=check_id)
            if is_expired:
                raise PaymentExpiredException

            cost = 0
            for (event_id, number_of_tickets) in check.events.items():
                event_id = int(event_id)
                event = await EventsService.get_event_info(self.uow, event_id)
                cost += event.price * number_of_tickets

            # receive payment from <card, cvv> summ = cost

            await ChecksService.update_check_info(self.uow, check_id, is_payed=True)

            await self.uow.commit()

