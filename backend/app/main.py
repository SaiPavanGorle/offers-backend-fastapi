from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.public import router as public_router
from app.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    await seed_data()
    yield


app = FastAPI(title="Proximity Offers API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.0.2.2:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(public_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
