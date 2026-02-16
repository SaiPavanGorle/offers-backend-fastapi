from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.public import router as public_router
from app.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    await seed_data()
    yield


app = FastAPI(title="Proximity Offers API", version="1.0.0", lifespan=lifespan)
app.include_router(public_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
