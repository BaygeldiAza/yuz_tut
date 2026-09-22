from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid6

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.user import User

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="conversations",
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversations",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_conversations_user_updated",
            "user_id",
            "updated_at",
        ),
    )