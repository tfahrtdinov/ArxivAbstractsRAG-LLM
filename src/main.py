from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import ProgrammingError

from src.dependencies import get_db_size
from src.routers import ask


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    try:
        size = get_db_size()
    except ProgrammingError:
        raise RuntimeError("Database doesn't exist")
    else:
        if size == 0:
            raise RuntimeError("Database exists but is empty")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ask.router, prefix="/ask", tags=["ask"])
