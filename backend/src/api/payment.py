from fastapi import APIRouter, Depends

from schemas.payment import PaymentSchema, RefundSchema
from services.auth.dependencies import get_current_user_id
from usecases.dependencies import BookingCase, CheckCase

router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)


@router.post("/{check_id}")
async def confirm(
    check_id: int,
    payment_info: PaymentSchema,
    check_case: CheckCase,
    user_id: int = Depends(get_current_user_id),
):
    await check_case.commit_payment(
        check_id, user_id, payment_info.card, payment_info.cvv
    )
    return {"status": "ok"}


@router.patch("/{booking_id}")
async def refund(
    booking_id: int,
    refund_info: RefundSchema,
    booking_case: BookingCase,
    user_id: int = Depends(get_current_user_id),
):
    await booking_case.refund(booking_id, user_id, refund_info.card)
    return {"status": "ok"}
