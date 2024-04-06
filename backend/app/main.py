from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(auth_router)

