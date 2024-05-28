from fastapi import APIRouter, Depends

from schemas.checks import CheckAddSchema
from services.auth.dependencies import get_current_user_id
from usecases.dependencies import BookingCase, CheckCase

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("/")
async def get_bookings_list(
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    return await booking_case.get_list(user_id)


@router.get("/{booking_id}")
async def get_booking_info(
    booking_id: int,
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    return await booking_case.get_info(booking_id, user_id)


@router.get("/user/{target_user_id}")
async def get_bookings_list_by_user_id(
    target_user_id: int,
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    return await booking_case.get_list_by_user(target_user_id, user_id)


@router.get("/my/get")
async def get_bookings_list_by_current_user_id(
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    return await booking_case.get_list_by_current_user(user_id)


@router.post("/")
async def book(
    events: CheckAddSchema,
    check_case: CheckCase,
    user_id: int = Depends(get_current_user_id),
):
    await check_case.create(user_id, events)
    # redirect to payment
    return {"status": "ok"}


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    await booking_case.delete(booking_id, user_id)
    return {"status": "ok"}
