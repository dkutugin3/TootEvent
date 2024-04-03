from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter(tags=["Found papa"])

#
# @router.get("/")
# def a():
#     return 21