from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


class SUserRegister(BaseModel):
    email: Annotated[EmailStr, StringConstraints(max_length=30)]
    name: Annotated[str, StringConstraints(max_length=30)]
    password: str


class SUserAuth(BaseModel):
    email: Annotated[EmailStr, StringConstraints(max_length=30)]
    password: str
