from fastapi import APIRouter, Depends, UploadFile

from usecases.dependencies import UserCase
from utils.file_manager import FileUploader as Fu
from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/avatar/me")
async def upload_my_avatar(
        avatar: UploadFile,
        user_id: int = Depends(get_current_user_id)
):
    await Fu.my_avatar_upload(avatar, user_id)
    return {"status": "ok"}


@router.delete("/avatar/me")
async def delete_my_avatar(
        user_id: int = Depends(get_current_user_id)
):
    await Fu.delete_my_avatar(user_id)
    return {"status": "ok"}


@router.get("/")
async def get_users_list(
        user_case: UserCase,
        user_id: int = Depends(get_current_user_id)
):
    return await user_case.get_list(user_id)