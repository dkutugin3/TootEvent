from typing import Annotated
from fastapi import Depends
from utils.unit_of_work import AbstractUOW, UOW

UOWDep = Annotated[AbstractUOW, Depends(UOW)]
