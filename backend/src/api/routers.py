from api.auth import router as auth_router
from api.events import router as events_router
from api.bookings import router as bookings_router
from api.payment import router as payment_router
from api.generate import router as generate_router

all_routers = [auth_router, events_router, bookings_router, payment_router, generate_router]
