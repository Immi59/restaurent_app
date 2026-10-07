from fastapi import APIRouter

from src.api.v1.routers.category import router as category_router
from src.api.v1.routers.admin import router as admin_router
from src.api.v1.routers.menu import router as menu_router
from src.api.v1.routers.client import router as client_router
from src.api.v1.routers.manager import router as manager_router
from src.api.v1.routers.admin_permission import router as admin_permission_router
from src.api.v1.routers.manager_permission import router as manager_permission_router

main_router = APIRouter()

main_router.include_router(category_router)
main_router.include_router(admin_router)
main_router.include_router(menu_router)
main_router.include_router(client_router)
main_router.include_router(manager_router)
main_router.include_router(admin_permission_router)
main_router.include_router(manager_permission_router)
