from fastapi import FastAPI

from ai.pipeline import run_pipeline, get_searcher
from .schemas import QueryRequest, QueryResponse

app = FastAPI()


@app.on_event("startup")
def warm_up():
    get_searcher()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = run_pipeline(
        query=request.query,
        user_lat=request.user_lat,
        user_lon=request.user_lon,
    )
    return result
