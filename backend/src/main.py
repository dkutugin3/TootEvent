from fastapi import FastAPI
import uvicorn
from api.routers import all_routers

app = FastAPI(title="TootEvent")
for router in all_routers:
    app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
