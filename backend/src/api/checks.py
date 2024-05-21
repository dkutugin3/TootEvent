from fastapi import APIRouter, Depends

from schemas.checks import CheckAddSchema
from usecases.dependencies import BookingCase
from usecases.dependencies import CheckCase

from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/checks",
    tags=["Checks"],
)


@router.get("/{user_id}")
async def get_checks_list(
        target_user_id: int,
        is_payed: bool,
        check_case: CheckCase,
        user_id: int = Depends(get_current_user_id),
):
    return await check_case.get_list_by_user(user_id, target_user_id, is_payed=is_payed)


@router.get("/")
async def get_my_checks_list(
        is_payed: bool,
        check_case: CheckCase,
        user_id: int = Depends(get_current_user_id),
):
    return await check_case.get_list_by_current_user(user_id, is_payed=is_payed)


