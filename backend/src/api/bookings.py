from fastapi import APIRouter, Depends

from usecases.dependencies import BookingCase

from services.auth.dependencies import get_current_user_id


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


@router.get("/my/")
async def get_bookings_list_by_current_user_id(
        booking_case: BookingCase,
        user_id: int = Depends(get_current_user_id),
):
    return await booking_case.get_list_by_current_user(user_id)


@router.post("/{event_id}{number_of_tickets}")
async def buy(
        event_id: int,
        number_of_tickets: int,
        booking_case: BookingCase,
        user_id: int = Depends(get_current_user_id),
):
    await booking_case.buy(event_id, number_of_tickets, user_id)
    # redirect to payment
    return {"status": "ok"}


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        booking_case: BookingCase,
        user_id: int = Depends(get_current_user_id)
):
    await booking_case.delete(booking_id, user_id)
    return {"status": "ok"}
