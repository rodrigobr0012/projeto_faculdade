from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.seed import seed_database
from .routes.car_routes import router as car_router

app = FastAPI(title="BuyMove API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(car_router)


@app.on_event("startup")
async def startup_event() -> None:
    await seed_database()


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {"message": "BuyMove API is running"}
