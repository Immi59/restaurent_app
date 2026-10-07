from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models import Admin


class Permission(StrEnum):
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"
    ADMIN_DELETE = "admin:delete"
    ADMIN_UPDATE = "admin:update"

    CATEGORY_READ = "category:read"
    CATEGORY_WRITE = "category:write"
    CATEGORY_DELETE = "category:delete"
    CATEGORY_UPDATE = "category:update"

    CLIENT_READ = "client:read"
    CLIENT_WRITE = "client:write"
    CLIENT_DELETE = "client:delete"
    CLIENT_UPDATE = "client:update"

    MANAGER_READ = "manager:read"
    MANAGER_WRITE = "manager:write"
    MANAGER_DELETE = "manager:delete"
    MANAGER_UPDATE = "manager:update"

    MENU_READ = "menu:read"
    MENU_WRITE = "menu:write"
    MENU_DELETE = "menu:delete"
    MENU_UPDATE = "menu:update"


def admin_has_permission(admin: "Admin", code: str) -> bool:
    return any(
        permission.code == code
        for role in admin.roles
        for permission in role.permissions
    )


def admin_has_role(admin: "Admin", name: str) -> bool:
    return any(role.name == name for role in admin.roles)
