"""create permissions and role_permissions tables"""

from alembic import op
import sqlalchemy as sa

revision = "20260517_01"
down_revision = "20260516_02"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(), nullable=False, unique=True),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "role_permissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True)),
    )


def downgrade():
    op.drop_table("role_permissions")
    op.drop_table("permissions")
