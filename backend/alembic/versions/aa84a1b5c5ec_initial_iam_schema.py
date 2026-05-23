"""initial IAM schema

Revision ID: aa84a1b5c5ec
Revises:
Create Date: 2026-05-10 21:06:20.984005
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aa84a1b5c5ec"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create IAM base tables."""

    # -------------------------
    # USERS
    # -------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(150), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("apellido", sa.String(100), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )

    # -------------------------
    # ROLES
    # -------------------------
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(100), unique=True, nullable=False),
        sa.Column("descripcion", sa.String(255)),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )

    # -------------------------
    # TENANTS
    # -------------------------
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("razon_social", sa.String(200)),
        sa.Column("cuit", sa.String(20), unique=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )

    # -------------------------
    # USER-TENANT-ROLE
    # -------------------------
    op.create_table(
        "user_tenant_role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
    )


def downgrade() -> None:
    op.drop_table("user_tenant_role")
    op.drop_table("tenants")
    op.drop_table("roles")
    op.drop_table("users")
