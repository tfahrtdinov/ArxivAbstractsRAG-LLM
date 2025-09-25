from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.dependencies import get_db_size
from src.routers import ask


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    if get_db_size() == 0:
        raise RuntimeError("Database size is 0")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(ask.router, prefix="/ask", tags=["ask"])

