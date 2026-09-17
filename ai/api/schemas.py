from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    user_lat: float | None = None
    user_lon: float | None = None


class QueryResponse(BaseModel):
    answer: str
    understanding: dict
    results: list[dict]
