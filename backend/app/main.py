from fastapi import FastAPI

app = FastAPI(title="Pluralia API")

@app.get("/health")
def health():
    return {"status": "ok"}
