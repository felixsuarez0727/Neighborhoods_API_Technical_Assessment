from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routers import v1

app = FastAPI()
app.include_router(v1.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)