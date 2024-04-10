from fastapi import APIRouter, Response, Depends

from schemas.auth import UserRegisterSchema, UserLoginSchema, UserInfoSchema
from services.auth.dependencies import UOWDep, get_current_user_id
from services.users import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(uow: UOWDep, user_data: UserRegisterSchema, response: Response):
    await UsersService.register_user(uow=uow, user=user_data, response=response)
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    uow: UOWDep,
    user_data: UserLoginSchema,
    response: Response,
):
    await UsersService.login_user(uow, user_data, response=response)
    return {"status": "ok"}


@router.post("/logout")
async def logout_user(response: Response):
    UsersService.logout_user(response=response)
    return {"status": "ok"}


@router.get("/info")
async def get_user_info(
    uow: UOWDep, user_id: int = Depends(get_current_user_id)
) -> UserInfoSchema:
    return await UsersService.get_user_info(uow=uow, user_id=user_id)
