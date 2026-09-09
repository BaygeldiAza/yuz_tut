from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine

app = FastAPI(
    title="Yuz-Tut-Backend",
    description="Backend API for Yuz-Tut",
    version="1.0.0",
    )

@app.get("/")
def message():
    return {"Yuz Tut": "Backend"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/database")
async def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
