import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.src.infrastructure.api.routes import router
from services.api.src.infrastructure.database.db import init_db

app = FastAPI(title="Pluralia API")

cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

init_db()


@app.get("/health")
def health():
    return {"status": "ok"}

