from fastapi import FastAPI

from src.routers import ask

app = FastAPI()
app.include_router(ask.router, prefix="/ask", tags=["ask"])
