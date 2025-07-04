import asyncio
import logging
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from core.config import settings
from core.database import Base

# Добавляем корень проекта в sys.path для импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Загружаем .env
load_dotenv()

logger = logging.getLogger(__name__)


def load_all_models():
    """
    Сканирует директорию apps/ и загружает модели из всех apps/<service>/models
    """
    apps_dir = Path(__file__).parent.parent / "apps"
    if not apps_dir.exists():
        raise FileNotFoundError("Директория apps/ не найдена")

    for service_dir in apps_dir.iterdir():
        if not service_dir.is_dir():
            continue

        service_name = service_dir.name
        models_dir = service_dir / "models"

        if not models_dir.exists():
            continue

        for model_file in models_dir.iterdir():
            file_name = model_file.stem
            if file_name.startswith('__') and file_name.endswith('__') or model_file.suffix != '.py':
                continue
            try:
                models_file_module = __import__(f"apps.{service_name}.models.{file_name}", fromlist=["*"])
                # Собираем все объекты, которые могут быть моделями
                for name in filter(
                        lambda var: var.endswith('Model') and var != Base.__name__,
                        dir(models_file_module)
                ):
                    obj = getattr(models_file_module, name)
                    if isinstance(obj, type) and issubclass(obj, Base) and obj is not Base:
                        obj.metadata    # Регистрируем модель
            except ImportError as e:
                logger.warning(f"Предупреждение: Не удалось загрузить модели для сервиса {service_name}: {e}")
                continue


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


config.set_main_option("sqlalchemy.url", settings.ASYNC_DATABASE_URL)

load_all_models()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
