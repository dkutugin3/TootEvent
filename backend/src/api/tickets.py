from fastapi import APIRouter, Depends

from usecases.dependencies import TicketCase

from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.get("/")
async def get_tickets_list(
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id),
):
    return await ticket_case.get_list(user_id)


@router.get("/{ticket_id}")
async def get_ticket_info(
        ticket_id: int,
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id),
):
    return await ticket_case.get_info(ticket_id, user_id)


@router.get("/user/{target_user_id}")
async def get_tickets_list_by_user_id(
        target_user_id: int,
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id),
):
    return await ticket_case.get_list_by_user(target_user_id, user_id)


@router.get("/my/")
async def get_tickets_list_by_current_user_id(
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id),
):
    return await ticket_case.get_list_by_current_user(user_id)


@router.delete("/refund/{ticket_id}")
async def refund_ticket(
        ticket_id: int,
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id)
):
    await ticket_case.refund(ticket_id, user_id)
    return {"status": "ok"}


@router.delete("/{ticket_id}")
async def delete_ticket(
        ticket_id: int,
        ticket_case: TicketCase,
        user_id: int = Depends(get_current_user_id)
):
    await ticket_case.delete(ticket_id, user_id)
    return {"status": "ok"}
