from typing import Annotated

from fastapi import Depends

from domain.usecases.booking import AbstractBookingUseCase
from domain.usecases.check import AbstractCheckUseCase
from domain.usecases.event import AbstractEventUseCase
from domain.usecases.user import AbstractUserUseCase
from usecases.booking import BookingUseCase
from usecases.check import CheckUseCase
from usecases.event import EventUseCase
from usecases.user import UserUseCase

UserCase = Annotated[AbstractUserUseCase, Depends(UserUseCase)]
EventCase = Annotated[AbstractEventUseCase, Depends(EventUseCase)]
BookingCase = Annotated[AbstractBookingUseCase, Depends(BookingUseCase)]
CheckCase = Annotated[AbstractCheckUseCase, Depends(CheckUseCase)]
