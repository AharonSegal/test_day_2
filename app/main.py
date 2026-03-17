from fastapi import FastAPI
from app.routers import router

app = FastAPI(
    title="test_2",
    version="1.0.0"
)

app.include_router(router)