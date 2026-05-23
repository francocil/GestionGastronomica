"""create products table

Revision ID: 5eafcb130b7e
Revises: 20260516_02
Create Date: 2026-05-16 09:09:02.903036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5eafcb130b7e'
down_revision: Union[str, Sequence[str], None] = '20260516_02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
