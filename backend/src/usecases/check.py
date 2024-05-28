from domain.usecases.check import AbstractCheckUseCase
from schemas.checks import CheckAddSchema
from schemas.exceptions import (AccessForbiddenException,
                                CheckIsAlreadyPayedException,
                                EventAlreadyStartedException,
                                NotEnoughPlacesLeftException,
                                PaymentExpiredException)
from services.bookings import BookingsService
from services.checks import ChecksService
from services.events import EventsService
from services.users import UsersService
from utils.date_manager import DateManager as Dm
from utils.dependencies import UOWDep


class CheckUseCase(AbstractCheckUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def create(self, user_id: int, data: CheckAddSchema):
        date = Dm.now()
        async with self.uow:
            check_id = await ChecksService.add_check(
                self.uow, user_id, data, Dm.date_to_string(date)
            )
            cost = 0
            for _event in data.events:
                event_id = _event["id"]
                number_of_tickets = _event["tickets"]

                event = await EventsService.get_event_info(self.uow, event_id)

                if event.places_left < number_of_tickets:
                    raise NotEnoughPlacesLeftException

                cost += number_of_tickets * event.price
                await EventsService.change_number_of_places_left(
                    self.uow, event_id, -number_of_tickets
                )
                await BookingsService.add_booking(
                    self.uow,
                    event_id,
                    user_id,
                    check_id,
                    number_of_tickets,
                    event.price,
                )

            await ChecksService.update_check_info(self.uow, check_id, total=cost)
            await self.uow.commit()

    async def commit_payment(self, check_id: int, user_id: int, card: int, cvv: int):
        date = Dm.now()
        async with self.uow:
            check = await ChecksService.get_check_info(self.uow, check_id)

            if user_id != check.user_id:
                raise AccessForbiddenException

            if check.is_payed:
                raise CheckIsAlreadyPayedException

            is_expired = await BookingsService.mark_if_expired(
                self.uow, check_id=check_id
            )
            if is_expired:
                raise PaymentExpiredException

            # receive payment from <card, cvv> <check.total>

            await ChecksService.update_check_info(self.uow, check_id, is_payed=True)

            await self.uow.commit()

    async def get_list_by_user(self, user_id: int, target_user_id: int, **filter_by):
        async with self.uow:
            if not await UsersService.user_is_moderator(self.uow, user_id):
                raise AccessForbiddenException
            checks_list = await ChecksService.get_checks_list(
                self.uow, user_id=target_user_id, **filter_by
            )

        return checks_list

    async def get_list_by_current_user(self, user_id: int, **filter_by):
        async with self.uow:
            checks_list = await ChecksService.get_checks_list(
                self.uow, user_id=user_id, **filter_by
            )

        return checks_list
