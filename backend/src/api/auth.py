from fastapi import APIRouter, Depends, Response

from schemas.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistException,
)
from services.auth import authenticate_user, create_access_token, get_password_hash
from repositories.users import UsersDAO
from api.dependencies import get_current_user
from models.users import Users
from schemas.auth import SUserRegister, SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        email=user_data.email, hashed_password=hashed_password, name=user_data.name
    )


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"status": True}


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
