import uvicorn
from api.routers import all_routers
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="TootEvent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in all_routers:
    app.include_router(router)
    
if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")
