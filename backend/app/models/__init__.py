# Este archivo asegura que TODOS los modelos se registren en SQLAlchemy.
# Es obligatorio para evitar errores de mapeo como:
# "expression 'Product' failed to locate a name ('Product')"

from app.models.base import Base
from app.models.user import User
from app.models.tenant import Tenant
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user_tenant_role import UserTenantRole
from app.models.product import Product
