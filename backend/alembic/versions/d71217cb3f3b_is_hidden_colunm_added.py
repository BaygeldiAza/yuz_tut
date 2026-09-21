"""is hidden column added

Revision ID: d71217cb3f3b
Revises: cb6cbeb84cad
Create Date: 2026-09-18 21:23:10.285987

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d71217cb3f3b"
down_revision: Union[str, Sequence[str], None] = "cb6cbeb84cad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "search_history",
        sa.Column(
            "is_hidden",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_index(
        "ix_search_history_is_hidden",
        "search_history",
        ["is_hidden"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_search_history_is_hidden",
        table_name="search_history",
    )

    op.drop_column(
        "search_history",
        "is_hidden",
    )