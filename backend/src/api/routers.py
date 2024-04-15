from api.auth import router as auth_router
from api.events import router as events_router

all_routers = [auth_router, events_router]
