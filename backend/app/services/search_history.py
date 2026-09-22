from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.search_history import SearchHistoryRepository


class SearchHistoryService:
    def __init__(self, session: AsyncSession):
        self.repository = SearchHistoryRepository(session)

    async def create_history(self, user_id: UUID, query: str):

        return await self.repository.create(
            user_id=user_id,
            query=query,
        )

    async def get_user_history(self, user_id:UUID):

        return await self.repository.get_by_user(user_id=user_id)

    async def get_histort_item(self, search_id: UUID, user_id: UUID):

        return await self.repository.get_by_id(search_id=search_id, user_id=user_id)

    async def hide_history_item(self, search_id: UUID, user_id: UUID)->bool:

        return await self.repository.hide_by_id(search_id=search_id, user_id=user_id)