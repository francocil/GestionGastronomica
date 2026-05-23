"""create products table

Revision ID: 20260516_02
Revises: aa84a1b5c5ec
Create Date: 2026-05-16 09:10:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260516_02"
down_revision: Union[str, Sequence[str], None] = "aa84a1b5c5ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create products table."""
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False, index=True),

        sa.Column("nombre", sa.String(length=150), nullable=False, index=True),
        sa.Column("descripcion", sa.String(length=500)),
        sa.Column("precio", sa.Float(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),

        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )


def downgrade() -> None:
    """Downgrade schema: drop products table."""
    op.drop_table("products")
