from datetime import datetime
from uuid import UUID

from pydantic import BaseModel,ConfigDict

class SearchHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    query: str
    created_at: datetime

    