from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.search_history import SearchHistoryResponse
from app.services.search_history import SearchHistoryService

# Replace this import with the actual location
# of your existing authentication dependency.
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/v1/search-history",
    tags=["Search History"],
)


@router.get(
    "",
    response_model=list[SearchHistoryResponse],
)
async def get_search_history(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = SearchHistoryService(db)

    return await service.get_user_history(
        user_id=current_user.id,
    )


@router.delete(
    "/{search_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def hide_search_history(
    search_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = SearchHistoryService(db)

    hidden = await service.hide_history_item(
        search_id=search_id,
        user_id=current_user.id,
    )

    if not hidden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search history item not found",
        )