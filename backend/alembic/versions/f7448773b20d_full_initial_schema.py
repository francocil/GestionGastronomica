"""full_initial_schema

Revision ID: 3fbf3a2ff71c
Revises:
Create Date: 2026-05-25 12:14:56.138521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fbf3a2ff71c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # === EMPRESAS / CORE FISCALES ===
    op.create_table(
        "empresas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cuit_cuil", sa.String(length=20), nullable=False),
        sa.Column("razon_social", sa.String(length=255), nullable=False),
        sa.Column("nombre_fantasia", sa.String(length=255), nullable=True),
        sa.Column("direccion_fiscal", sa.String(length=255), nullable=True),
        sa.Column("email_contacto", sa.String(length=150), nullable=True),
        sa.Column("telefono_contacto", sa.String(length=50), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("configuracion_fiscal_id", sa.Integer(), nullable=True),
        sa.Column("configuracion_delivery_id", sa.Integer(), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.Column("logo_url", sa.String(length=255), nullable=True),
        sa.Column("timezone", sa.String(length=100), nullable=True),
        sa.Column("moneda_id", sa.Integer(), nullable=True),
        sa.Column("condicion_iva", sa.String(length=50), nullable=True),
        sa.Column("ingresos_brutos", sa.String(length=50), nullable=True),
        sa.Column("plan_suscripcion_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_empresa_activo", "empresas", ["activo"], unique=False)
    op.create_index("idx_empresa_cuit_cuil", "empresas", ["cuit_cuil"], unique=True)
    op.create_index(op.f("ix_empresas_id"), "empresas", ["id"], unique=False)

    # === TABLAS IAM AUXILIARES ===
    op.create_table(
        "estado_usuario",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_estado_usuario_id"), "estado_usuario", ["id"], unique=False
    )

    op.create_table(
        "mfa_estado",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_mfa_estado_id"), "mfa_estado", ["id"], unique=False)

    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_permissions_id"), "permissions", ["id"], unique=False)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)

    # === TENANTS / TIPO_USUARIO ===
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("razon_social", sa.String(length=200), nullable=True),
        sa.Column("cuit", sa.String(length=20), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cuit"),
    )
    op.create_index(op.f("ix_tenants_id"), "tenants", ["id"], unique=False)

    op.create_table(
        "tipo_usuario",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tipo_usuario_id"), "tipo_usuario", ["id"], unique=False)

    # === CATEGORIAS / SUCURSALES / UNIDADES_MEDIDA ===
    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.String(length=300), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_categorias_tenant_id"), "categorias", ["tenant_id"], unique=False
    )

    op.create_table(
        "sucursales",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("direccion", sa.String(length=300), nullable=True),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sucursales_tenant_id"), "sucursales", ["tenant_id"], unique=False
    )

    op.create_table(
        "unidades_medida",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("abreviatura", sa.String(length=20), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_unidades_medida_tenant_id"),
        "unidades_medida",
        ["tenant_id"],
        unique=False,
    )

    # === USERS ===
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("tipo_usuario_id", sa.Integer(), nullable=False),
        sa.Column("estado_usuario_id", sa.Integer(), nullable=False),
        sa.Column("mfa_estado_id", sa.Integer(), nullable=False),
        sa.Column("intentos_fallidos", sa.Integer(), nullable=False),
        sa.Column("fecha_bloqueo", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "ultimo_cambio_password", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column("fecha_ultimo_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["estado_usuario_id"], ["estado_usuario.id"]),
        sa.ForeignKeyConstraint(["mfa_estado_id"], ["mfa_estado.id"]),
        sa.ForeignKeyConstraint(["tipo_usuario_id"], ["tipo_usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # índices EXACTOS del modelo
    op.create_index("idx_usuario_email", "users", ["email"], unique=True)
    op.create_index(
        "idx_usuario_empresa_id", "users", ["empresa_id"], unique=False
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # === ROLE_PERMISSIONS (PIVOT) ===
    op.create_table(
        "role_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission_id"], ["permissions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_role_permissions_id"), "role_permissions", ["id"], unique=False
    )

    # === INSUMOS ===
    op.create_table(
        "insumos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.String(length=300), nullable=True),
        sa.Column("unidad_medida_id", sa.Integer(), nullable=False),
        sa.Column("costo_unitario", sa.Float(), nullable=False),
        sa.Column("stock_actual", sa.Float(), nullable=False),
        sa.Column("stock_minimo", sa.Float(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["unidad_medida_id"], ["unidades_medida.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_insumos_tenant_id"), "insumos", ["tenant_id"], unique=False
    )
    op.create_index(
        "idx_insumos_unidad_medida_id",
        "insumos",
        ["unidad_medida_id"],
        unique=False,
    )

    # === PRODUCTS ===
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=True),
        sa.Column("unidad_medida_id", sa.Integer(), nullable=True),
        sa.Column("sucursal_id", sa.Integer(), nullable=True),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.String(length=300), nullable=True),
        sa.Column("sku", sa.String(length=50), nullable=True),
        sa.Column("precio", sa.Float(), nullable=False),
        sa.Column("costo", sa.Float(), nullable=True),
        sa.Column("imagen_url", sa.String(length=300), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"]),
        sa.ForeignKeyConstraint(["sucursal_id"], ["sucursales.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["unidad_medida_id"], ["unidades_medida.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=False)
    op.create_index(
        op.f("ix_products_tenant_id"), "products", ["tenant_id"], unique=False
    )
    op.create_index(
        "idx_products_categoria_id", "products", ["categoria_id"], unique=False
    )
    op.create_index(
        "idx_products_unidad_medida_id",
        "products",
        ["unidad_medida_id"],
        unique=False,
    )
    op.create_index(
        "idx_products_sucursal_id", "products", ["sucursal_id"], unique=False
    )

    # === USER_TENANT_ROLE (PIVOT) ===
    op.create_table(
        "user_tenant_role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
    )
    op.create_index(
        op.f("ix_user_tenant_role_id"), "user_tenant_role", ["id"], unique=False
    )

    # === RECETAS ===
    op.create_table(
        "recetas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.String(length=300), nullable=True),
        sa.Column("tiempo_preparacion", sa.Integer(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["producto_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("producto_id"),
    )
    op.create_index(
        op.f("ix_recetas_tenant_id"), "recetas", ["tenant_id"], unique=False
    )

    # === STOCK_MOVIMIENTOS ===
    op.create_table(
        "stock_movimientos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("insumo_id", sa.Integer(), nullable=False),
        sa.Column("sucursal_id", sa.Integer(), nullable=False),
        sa.Column("tipo_movimiento", sa.String(length=20), nullable=False),
        sa.Column("cantidad", sa.Float(), nullable=False),
        sa.Column("motivo", sa.String(length=200), nullable=True),
        sa.Column("referencia", sa.String(length=100), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["insumo_id"], ["insumos.id"]),
        sa.ForeignKeyConstraint(["sucursal_id"], ["sucursales.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_stock_movimientos_tenant_id"),
        "stock_movimientos",
        ["tenant_id"],
        unique=False,
    )
    op.create_index(
        "idx_stock_movimientos_insumo_id",
        "stock_movimientos",
        ["insumo_id"],
        unique=False,
    )
    op.create_index(
        "idx_stock_movimientos_sucursal_id",
        "stock_movimientos",
        ["sucursal_id"],
        unique=False,
    )

    # === RECETA_DETALLE ===
    op.create_table(
        "receta_detalle",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("receta_id", sa.Integer(), nullable=False),
        sa.Column("insumo_id", sa.Integer(), nullable=False),
        sa.Column("unidad_medida_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Float(), nullable=False),
        sa.Column("costo_parcial", sa.Float(), nullable=False),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "fecha_actualizacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("eliminado", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["insumo_id"], ["insumos.id"]),
        sa.ForeignKeyConstraint(["receta_id"], ["recetas.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["unidad_medida_id"], ["unidades_medida.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_receta_detalle_tenant_id"),
        "receta_detalle",
        ["tenant_id"],
        unique=False,
    )
    op.create_index(
        "idx_receta_detalle_receta_id",
        "receta_detalle",
        ["receta_id"],
        unique=False,
    )
    op.create_index(
        "idx_receta_detalle_insumo_id",
        "receta_detalle",
        ["insumo_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop in reverse dependency order
    op.drop_index("idx_receta_detalle_insumo_id", table_name="receta_detalle")
    op.drop_index("idx_receta_detalle_receta_id", table_name="receta_detalle")
    op.drop_index(op.f("ix_receta_detalle_tenant_id"), table_name="receta_detalle")
    op.drop_table("receta_detalle")

    op.drop_index("idx_stock_movimientos_sucursal_id", table_name="stock_movimientos")
    op.drop_index("idx_stock_movimientos_insumo_id", table_name="stock_movimientos")
    op.drop_index(
        op.f("ix_stock_movimientos_tenant_id"), table_name="stock_movimientos"
    )
    op.drop_table("stock_movimientos")

    op.drop_index(op.f("ix_recetas_tenant_id"), table_name="recetas")
    op.drop_table("recetas")

    op.drop_index(op.f("ix_user_tenant_role_id"), table_name="user_tenant_role")
    op.drop_table("user_tenant_role")

    op.drop_index("idx_products_sucursal_id", table_name="products")
    op.drop_index("idx_products_unidad_medida_id", table_name="products")
    op.drop_index("idx_products_categoria_id", table_name="products")
    op.drop_index(op.f("ix_products_tenant_id"), table_name="products")
    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_table("products")

    op.drop_index("idx_insumos_unidad_medida_id", table_name="insumos")
    op.drop_index(op.f("ix_insumos_tenant_id"), table_name="insumos")
    op.drop_table("insumos")

    op.drop_index(op.f("ix_role_permissions_id"), table_name="role_permissions")
    op.drop_table("role_permissions")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index("idx_usuario_empresa_id", table_name="users")
    op.drop_index("idx_usuario_email", table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_unidades_medida_tenant_id"), table_name="unidades_medida")
    op.drop_table("unidades_medida")

    op.drop_index(op.f("ix_sucursales_tenant_id"), table_name="sucursales")
    op.drop_table("sucursales")

    op.drop_index(op.f("ix_categorias_tenant_id"), table_name="categorias")
    op.drop_table("categorias")

    op.drop_index(op.f("ix_tipo_usuario_id"), table_name="tipo_usuario")
    op.drop_table("tipo_usuario")

    op.drop_index(op.f("ix_tenants_id"), table_name="tenants")
    op.drop_table("tenants")

    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_table("roles")

    op.drop_index(op.f("ix_permissions_id"), table_name="permissions")
    op.drop_table("permissions")

    op.drop_index(op.f("ix_mfa_estado_id"), table_name="mfa_estado")
    op.drop_table("mfa_estado")

    op.drop_index(op.f("ix_estado_usuario_id"), table_name="estado_usuario")
    op.drop_table("estado_usuario")

    op.drop_index(op.f("ix_empresas_id"), table_name="empresas")
    op.drop_index("idx_empresa_cuit_cuil", table_name="empresas")
    op.drop_index("idx_empresa_activo", table_name="empresas")
    op.drop_table("empresas")
    # ### end Alembic commands ###
