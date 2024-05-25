from api.auth import router as auth_router
from api.events import router as events_router
from api.bookings import router as bookings_router
from api.payment import router as payment_router
from api.generate import router as generate_router
from api.checks import router as checks_router
from api.users import router as users_router

all_routers = [auth_router, users_router, events_router, bookings_router, checks_router, payment_router, generate_router]
