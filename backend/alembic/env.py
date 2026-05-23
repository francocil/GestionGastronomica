from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar tu Base declarativa
from app.models.base import Base

# Importar settings para obtener DATABASE_URL real
from app.core.config import settings


# ---------------------------------------------------------
# Configuración base de Alembic
# ---------------------------------------------------------
config = context.config

# Sobrescribir sqlalchemy.url con tu DATABASE_URL real
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata


# ---------------------------------------------------------
# Modo OFFLINE
# ---------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Ejecuta migraciones en modo offline.
    No requiere conexión real a la base.
    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Modo ONLINE
# ---------------------------------------------------------
def run_migrations_online() -> None:
    """
    Ejecuta migraciones en modo online.
    Requiere conexión real a la base.
    """

    # 🔥 FIX DEFINITIVO PARA PYLANCE:
    # get_section() puede devolver None → engine_from_config NO acepta None
    ini_section = config.get_section(config.config_ini_section) or {}

    connectable = engine_from_config(
        ini_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detecta cambios en tipos de columnas
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# Ejecutar según modo
# ---------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
