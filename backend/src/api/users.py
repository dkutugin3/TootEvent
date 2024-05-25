from fastapi import APIRouter, Depends, UploadFile

from usecases.dependencies import UserCase
from utils.file_manager import FileUploader as Fu
from services.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/{user_id}/avatar")
async def upload_avatar(
        target_user_id: int,
        avatar: UploadFile,
        user_case: UserCase,
        user_id: int = Depends(get_current_user_id)
):
    await Fu.avatar_upload(target_user_id, avatar, user_case, user_id)
    return {"status": "ok"}


@router.post("/avatar/me")
async def upload_my_avatar(
        avatar: UploadFile,
        user_case: UserCase,
        user_id: int = Depends(get_current_user_id)
):
    await Fu.my_avatar_upload(avatar, user_case, user_id)
    return {"status": "ok"}
