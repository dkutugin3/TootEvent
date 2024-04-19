from api.auth import router as auth_router
from api.events import router as events_router
from api.bookings import router as bookings_router
from api.tickets import router as tickets_router

all_routers = [auth_router, events_router, bookings_router, tickets_router]
