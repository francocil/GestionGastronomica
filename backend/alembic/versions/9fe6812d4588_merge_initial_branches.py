"""merge initial branches

Revision ID: 9fe6812d4588
Revises: 20260517_01, 5eafcb130b7e
Create Date: 2026-05-18 21:28:21.484911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fe6812d4588'
down_revision: Union[str, Sequence[str], None] = ('20260517_01', '5eafcb130b7e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
