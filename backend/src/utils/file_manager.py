from domain.usecases.event import AbstractEventUseCase
from domain.usecases.user import AbstractUserUseCase
from fastapi import UploadFile
from schemas.exceptions import BadFileException


class FileUploader:
    @staticmethod
    async def poster_upload(
        event_id: int,
        poster: UploadFile,
        event_case: AbstractEventUseCase,
        user_id: int,
    ):
        if poster.content_type != "image/jpeg":
            raise BadFileException
        with open(f"../resources/posters/poster_{event_id}.jpeg", "wb") as file:
            file.write(await poster.read())
        await event_case.edit_info(
            event_id,
            user_id,
            poster_path=f"../resources/posters/poster_{event_id}.jpeg",
        )

    @staticmethod
    async def avatar_upload(
        target_user_id: int,
        avatar: UploadFile,
        user_case: AbstractUserUseCase,
        user_id: int,
    ):
        if avatar.content_type != "image/jpeg":
            raise BadFileException
        with open(f"../resources/avatars/avatar_{target_user_id}.jpeg", "wb") as file:
            file.write(await avatar.read())
        await user_case.edit_info(
            user_id,
            target_user_id,
            avatar_path=f"../resources/avatars/avatar_{target_user_id}.jpeg",
        )

    @staticmethod
    async def my_avatar_upload(
        avatar: UploadFile, user_case: AbstractUserUseCase, user_id: int
    ):
        if avatar.content_type != "image/jpeg":
            raise BadFileException
        with open(f"../resources/avatars/avatar_{user_id}.jpeg", "wb") as file:
            file.write(await avatar.read())
        await user_case.edit_my_info(
            user_id, avatar_path=f"../resources/avatars/avatar_{user_id}.jpeg"
        )

    @staticmethod
    async def get_poster(event_id: int, event_case: AbstractEventUseCase) -> bytes:
        event = await event_case.get_info(event_id)
        with open(event.poster_path, "rb") as file:
            return file.read()

    @staticmethod
    async def get_my_avatar(user_id: int, user_case: AbstractUserUseCase) -> bytes:
        user = await user_case.get_my_info(user_id)
        with open(user.avatar_path, "rb") as file:
            return file.read()
