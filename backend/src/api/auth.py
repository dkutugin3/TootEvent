from fastapi import APIRouter, Response, Depends

from schemas.auth import UserRegisterSchema, UserLoginSchema, UserInfoSchema
from usecases.user import UserUseCase
from services.auth.dependencies import get_current_user_id
from usecases.dependencies import UserCase, EventCase
from services.users import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(
    user_data: UserRegisterSchema, response: Response, user_case: UserCase
):
    await user_case.registrate(user=user_data, response=response)
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    user_data: UserLoginSchema, response: Response, user_case: UserCase
):
    await user_case.login(user_data, response=response)
    return {"status": "ok"}


@router.post("/logout")
async def logout_user(response: Response, user_case: UserCase):
    user_case.logout(response=response)
    return {"status": "ok"}


@router.get("/info")
async def get_user_info(
    user_case: UserCase, user_id: int = Depends(get_current_user_id)
) -> UserInfoSchema:
    return await user_case.get_info(user_id=user_id)
