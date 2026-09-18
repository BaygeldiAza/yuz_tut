from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.search_history import SearchHistory


class SearchHistoryRepository:
    def __init__(self, session: AsyncSession):
        select.session = session

    async def create(self, user_id: UUID, query: str)->SearchHistory:
        search_history = SearchHistory(
            user_id=user_id,
            query=query
        )
        self.session.add(search_history)

        await self.session.flush()
        await self.session.refresh(search_history)

        return search_history

    async def get_by_user(self, user_id: UUID)->list[SearchHistory]:
        statement=(
            select(SearchHistory).where(
                SearchHistory.user_id == user_id,
                SearchHistory.is_hidden.is_(False),
            ).order_by(
                SearchHistory.created_at.desc()
            )
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_id(self, search_id: UUID, user_id: UUID)->SearchHistory|None:
        statement=(
            select(SearchHistory).where(
                SearchHistory.id == search_id,
                SearchHistory.user_id == user_id,
                SearchHistory.is_hidden.is_(False),
            )
        )
        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def hide_by_id(self, search_id: UUID, user_id:UUID)->bool:

        statement=(
            update(SearchHistory).where(
                SearchHistory.id==search_id,
                SearchHistory.user_id==user_id,
                SearchHistory.is_hidden.is_(False), 
            ).values(
                is_hidden=True
            )
        )

        result = await self.session.execute(statement)

        return result.rowcount > 0