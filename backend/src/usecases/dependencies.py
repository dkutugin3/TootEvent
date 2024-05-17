from typing import Annotated

from fastapi import Depends

from domain.usecases.booking import AbstractBookingUseCase
from domain.usecases.event import AbstractEventUseCase
from domain.usecases.user import AbstractUserUseCase
from usecases.event import EventUseCase
from usecases.user import UserUseCase
from usecases.booking import BookingUseCase

UserCase = Annotated[AbstractUserUseCase, Depends(UserUseCase)]
EventCase = Annotated[AbstractEventUseCase, Depends(EventUseCase)]
BookingCase = Annotated[AbstractBookingUseCase, Depends(BookingUseCase)]
