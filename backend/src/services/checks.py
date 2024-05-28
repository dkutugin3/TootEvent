from typing import List

from pydantic import BaseModel

from schemas.checks import CheckAddSchema, CheckInfoSchema
from utils.date_manager import DateManager as Dm
from utils.unit_of_work import AbstractUOW


class ChecksService:
    @staticmethod
    async def add_check(
        uow: AbstractUOW,
        user_id: int,
        data: CheckAddSchema,
        date: str,
    ) -> int:
        check_id = await uow.checks.add_one(
            user_id=user_id,
            events=data.events,
            date=Dm.string_to_date(date),
            total=0,
            is_payed=False,
        )
        return check_id

    @staticmethod
    async def get_checks_list(uow: AbstractUOW, **filter_by) -> List[BaseModel]:
        checks = await uow.checks.find_all(**filter_by)
        for idx, check in enumerate(checks):

            is_expired = (
                Dm.add(Dm.now(), minutes=-30) > Dm.string_to_date(check.date)
            ) and (not check.is_payed)
            checks[idx] = CheckInfoSchema(**check.dict(), is_expired=is_expired)
        return checks

    @staticmethod
    async def get_check_info(uow: AbstractUOW, check_id: int) -> CheckInfoSchema:
        check = await uow.checks.find_one(id=check_id)

        is_expired = (
            Dm.add(Dm.now(), minutes=-30) > Dm.string_to_date(check.date)
        ) and (not check.is_payed)
        return CheckInfoSchema(**check.dict(), is_expired=is_expired)

    @staticmethod
    async def delete_check_by_id(uow: AbstractUOW, check_id: int):
        await uow.checks.delete_by_id(model_id=check_id)

    @staticmethod
    async def update_check_info(uow: AbstractUOW, check_id: int, **to_update):
        await uow.checks.update_by_id(check_id, **to_update)
