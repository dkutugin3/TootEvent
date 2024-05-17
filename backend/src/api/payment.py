from fastapi import APIRouter, Depends

from schemas.payment import PaymentSchema, RefundSchema
from usecases.dependencies import  BookingCase

from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)


@router.post("/{booking_id}")
async def confirm(
        booking_id: int,
        payment_info: PaymentSchema,
        booking_case: BookingCase,
        user_id: int = Depends(get_current_user_id)
):
    await booking_case.confirm(booking_id, user_id, payment_info.card, payment_info.cvv)
    return {"status": "ok"}


@router.patch("/{booking_id}")
async def refund(
        booking_id: int,
        refund_info: RefundSchema,
        booking_case: BookingCase,
        user_id: int = Depends(get_current_user_id)
):
    await booking_case.refund(booking_id, user_id, refund_info.card)
    return {"status": "ok"}
