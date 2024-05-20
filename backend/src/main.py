import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import all_routers

app = FastAPI(title="TootEvent")
for router in all_routers:
    app.include_router(router)
if __name__ == "__main__":
    origins = [
    "*",
]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")
