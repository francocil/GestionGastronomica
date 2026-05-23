from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.tenant import Tenant
from app.models.user import User
from app.models.user_tenant_role import UserTenantRole
from app.services.auth_service import hash_password


def run_seed():
    db: Session = next(get_db())

    print("=== Ejecutando SEED IAM + PBAC ===")

    # ============================================================
    # 1) Crear permisos base
    # ============================================================
    permisos_base = [
        "can_view_dashboard",
        "can_manage_products",
        "can_manage_users",
        "can_manage_tenants",
        "can_manage_roles",
        "can_manage_permissions",
    ]

    permisos_creados = {}

    for nombre in permisos_base:
        permiso = db.query(Permission).filter(Permission.nombre == nombre).first()
        if not permiso:
            permiso = Permission(nombre=nombre, descripcion=f"Permiso: {nombre}")
            db.add(permiso)
            db.commit()
            db.refresh(permiso)
        permisos_creados[nombre] = permiso

    print("✔ Permisos creados")

    # ============================================================
    # 2) Crear roles base
    # ============================================================
    roles = {
        "root_admin": ["can_view_dashboard", "can_manage_products", "can_manage_users",
                       "can_manage_tenants", "can_manage_roles", "can_manage_permissions"],
        "admin_empresa": ["can_view_dashboard", "can_manage_products", "can_manage_users"],
        "empleado": ["can_view_dashboard"],
    }

    roles_creados = {}

    for role_name, perms in roles.items():
        role = db.query(Role).filter(Role.nombre == role_name).first()
        if not role:
            role = Role(nombre=role_name, descripcion=f"Rol {role_name}", activo=True)
            db.add(role)
            db.commit()
            db.refresh(role)

        roles_creados[role_name] = role

        # Asignar permisos al rol
        for perm_name in perms:
            permiso = permisos_creados[perm_name]

            rp = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permiso.id
            ).first()

            if not rp:
                rp = RolePermission(role_id=role.id, permission_id=permiso.id)
                db.add(rp)
                db.commit()

    print("✔ Roles creados y permisos asignados")

    # ============================================================
    # 3) Crear tenant inicial
    # ============================================================
    tenant = db.query(Tenant).filter(Tenant.nombre == "Demo Company").first()
    if not tenant:
        tenant = Tenant(nombre="Demo Company", activo=True)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    print("✔ Tenant inicial creado")

    # ============================================================
    # 4) Crear usuario root
    # ============================================================
    user = db.query(User).filter(User.email == "admin@demo.com").first()
    if not user:
        user = User(
            email="admin@demo.com",
            password_hash=hash_password("admin123"),
            nombre="Root",
            apellido="Admin",
            activo=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    print("✔ Usuario root creado")

    # ============================================================
    # 5) Asignar usuario root al tenant con rol root_admin
    # ============================================================
    utr = db.query(UserTenantRole).filter(
        UserTenantRole.user_id == user.id,
        UserTenantRole.tenant_id == tenant.id
    ).first()

    if not utr:
        utr = UserTenantRole(
            user_id=user.id,
            tenant_id=tenant.id,
            role_id=roles_creados["root_admin"].id
        )
        db.add(utr)
        db.commit()

    print("✔ Usuario root asignado al tenant con rol root_admin")

    print("=== SEED COMPLETADO ===")


# ============================================================
# EJECUCIÓN DIRECTA DEL SEED
# ============================================================
if __name__ == "__main__":
    run_seed()

# desde backend
# python -m app.seed
