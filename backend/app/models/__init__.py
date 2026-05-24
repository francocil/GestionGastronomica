# Este archivo asegura que TODOS los modelos se registren en SQLAlchemy.
# Es obligatorio para que Alembic pueda ver todas las tablas y generar migraciones.

from app.models.base import Base

# Núcleo IAM / Multi-tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user_tenant_role import UserTenantRole

# Tablas IAM del SRS 4.3
from app.models.tipo_usuario import TipoUsuario
from app.models.estado_usuario import EstadoUsuario
from app.models.mfa_estado import MFAEstado

# Gestión gastronómica (según tus modelos actuales)
from app.models.categoria import Categoria
from app.models.unidad_medida import UnidadMedida
from app.models.insumo import Insumo
from app.models.receta import Receta
from app.models.receta_detalle import RecetaDetalle
from app.models.sucursal import Sucursal
from app.models.stock_movimiento import StockMovimiento

from app.models.product import Product
from app.models.empresa import Empresa
