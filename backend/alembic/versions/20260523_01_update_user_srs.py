from alembic import op
import sqlalchemy as sa


revision = "20260523_01_update_user_srs"
down_revision = "9fe6812d4588"
branch_labels = None
depends_on = None


def upgrade():
    # Campos nuevos del SRS
    op.add_column("users", sa.Column("empresa_id", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("username", sa.String(length=150), nullable=False))
    op.add_column("users", sa.Column("tipo_usuario_id", sa.Integer(), nullable=False))
    op.add_column("users", sa.Column("estado_usuario_id", sa.Integer(), nullable=False))
    op.add_column("users", sa.Column("mfa_estado_id", sa.Integer(), nullable=False))
    op.add_column("users", sa.Column("telefono", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("intentos_fallidos", sa.Integer(), server_default="0"))
    op.add_column("users", sa.Column("fecha_bloqueo", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("ultimo_cambio_password", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("fecha_ultimo_login", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("eliminado", sa.Boolean(), server_default="false"))

    # Foreign Keys del SRS
    op.create_foreign_key(
        None, "users", "empresas", ["empresa_id"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        None, "users", "tipo_usuario", ["tipo_usuario_id"], ["id"]
    )
    op.create_foreign_key(
        None, "users", "estado_usuario", ["estado_usuario_id"], ["id"]
    )
    op.create_foreign_key(
        None, "users", "mfa_estado", ["mfa_estado_id"], ["id"]
    )

    # Índices del SRS
    op.create_index("idx_usuario_email", "users", ["email"], unique=True)
    op.create_index("idx_usuario_empresa_id", "users", ["empresa_id"])


def downgrade():
    # Índices
    op.drop_index("idx_usuario_email", table_name="users")
    op.drop_index("idx_usuario_empresa_id", table_name="users")

    # Columnas (las FK se eliminan automáticamente al borrar columnas)
    op.drop_column("users", "empresa_id")
    op.drop_column("users", "username")
    op.drop_column("users", "tipo_usuario_id")
    op.drop_column("users", "estado_usuario_id")
    op.drop_column("users", "mfa_estado_id")
    op.drop_column("users", "telefono")
    op.drop_column("users", "intentos_fallidos")
    op.drop_column("users", "fecha_bloqueo")
    op.drop_column("users", "ultimo_cambio_password")
    op.drop_column("users", "fecha_ultimo_login")
    op.drop_column("users", "eliminado")
