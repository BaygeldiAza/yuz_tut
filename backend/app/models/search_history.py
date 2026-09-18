from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
from uuid6 import uuid6
from datetime import datetime, timezone 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database.base import Base
if TYPE_CHECKING:
    from app.models.user import User

class SearchHistory(Base):
    __tablename__ = "search_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6,
    )

    user_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="search_history",
    )

    __table_args__ = (
        Index(
            "ix_search_history_user_created",
            "user_id",
            "created_at",
        ),
    )

   