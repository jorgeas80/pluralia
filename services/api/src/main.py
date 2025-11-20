from fastapi import FastAPI
from services.api.src.infrastructure.api.routes import router
from services.api.src.infrastructure.database.db import init_db

app = FastAPI(title="Pluralia API")

app.include_router(router)

init_db()


@app.get("/health")
def health():
    return {"status": "ok"}

