from fastapi import APIRouter, Response, Depends

from schemas.events import EventInfoSchema, EventAddSchema
from utils.dependencies import UOWDep
from services.events import EventsService

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


# @router.get("/")
# async def get_events_list(uow: UOWDep, user_data: UserRegisterSchema, response: Response):
#     await UsersService.register_user(uow=uow, user=user_data, response=response)
#     return {"status": "ok"}


@router.post("/")
async def add_event(
    uow: UOWDep,
    event_data: EventAddSchema,
):
    await EventsService.add_event(uow, event_data,)
    return {"status": "ok"}


@router.get("/{event_id}")
async def get_event_info(
        uow: UOWDep, event_id: int) -> EventInfoSchema:
    return await EventsService.get_event_info(uow=uow, event_id=event_id)


# @router.delete("/{event_id}")
# async def delete_event(response: Response):
#     UsersService.logout_user(response=response)
#     return {"status": "ok"}
#
#
# @router.patch("/{event_id}")
# async def change_event_info(
#     uow: UOWDep, user_id: int = Depends(get_current_user_id)
# ) -> UserInfoSchema:
#     return await UsersService.get_user_info(uow=uow, user_id=user_id)
