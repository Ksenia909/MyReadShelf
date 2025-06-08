import logging
from pathlib import Path

from fastapi import APIRouter, FastAPI

logger = logging.getLogger(__name__)
APPS_DIR = Path(__file__).resolve().parent.parent / "apps"


def register_all_service_routers(root_router: APIRouter | FastAPI) -> None:
    for service_dir in APPS_DIR.iterdir():
        if not service_dir.is_dir():
            continue

        service_name = service_dir.name
        if service_name.startswith('__'):
            continue

        router_path = f"apps.{service_name}.api.routers"
        try:
            router_module = __import__(router_path, fromlist=["router"])
            router = getattr(router_module, "router", None)

            if router:
                root_router.include_router(router)
            else:
                logger.warning(f"No 'router' found in {router_path}")
        except ImportError as e:
            logger.error(f"Failed to import router from {router_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while loading {router_path}: {e}")
