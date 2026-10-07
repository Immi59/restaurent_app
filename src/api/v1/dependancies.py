import jwt
from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.repositories.manager_permission import ManagerRoleRepository, ManagerRolePermissionsRepository, ManagerPermissionRepository
from src.services.manager_permission import ManagerRolePermissionsService, ManagerPermissionService, ManagerRoleService
from src.core.exceptions import NotFoundError
from src.core.permissions import Permission, admin_has_permission
from src.core.security import get_client_id_from_token, get_admin_id_from_token
from src.database.models import Client, Admin
from src.database.session import get_session
from src.repositories.client import ClientRepository
from src.services.client import ClientService
from src.repositories.menu import MenuRepository
from src.services.menu import MenuService
from src.repositories.manager import ManagerRepository
from src.services.manager import ManagerService
from src.services.admin import AdminService
from src.repositories.admin import AdminRepository
from src.repositories.category import CategoryRepository
from src.services.category import CategoryService
from src.services.admin_permission import AdminRoleService, AdminPermissionService, AdminRolePermissionsService
from src.repositories.admin_permission import AdminRoleRepository, AdminPermissionRepository, AdminRolePermissionsRepository

client_access_token_scheme = HTTPBearer(scheme_name="client-access-token", auto_error=False)
admin_access_token_scheme = HTTPBearer(scheme_name="admin-access-token", auto_error=False)


def get_category_service() -> CategoryService:
    repository = CategoryRepository()
    return CategoryService(repository)


def get_admin_service() -> AdminService:
    repository = AdminRepository()
    return AdminService(repository)


def get_manager_service() -> ManagerService:
    repository = ManagerRepository()
    return ManagerService(repository)


def get_menu_service() -> MenuService:
    menu_repo = MenuRepository()
    category_repo = CategoryRepository()
    return MenuService(menu_repo, category_repo)


def get_client_service() -> ClientService:
    repository = ClientRepository()
    return ClientService(repository)


def get_admin_role_service() -> AdminRoleService:
    repository = AdminRoleRepository()
    return AdminRoleService(repository)


def get_admin_role_permission_service() -> AdminRolePermissionsService:
    role_repo = AdminRoleRepository()
    role_permission_repo = AdminRolePermissionsRepository()
    return AdminRolePermissionsService(role_repo, role_permission_repo)


def get_admin_permission_service() -> AdminPermissionService:
    repository = AdminPermissionRepository()
    return AdminPermissionService(repository)

def get_manager_role_service() -> ManagerRoleService:
    repository = ManagerRoleRepository()
    return ManagerRoleService(repository)


def get_manager_role_permission_service() -> ManagerRolePermissionsService:
    role_repo = ManagerRoleRepository()
    role_permission_repo = ManagerRolePermissionsRepository()
    return ManagerRolePermissionsService(role_repo, role_permission_repo)


def get_manager_permission_service() -> ManagerPermissionService:
    repository = ManagerPermissionRepository()
    return ManagerPermissionService(repository)


def get_current_client(
        credentials: HTTPAuthorizationCredentials | None = Security(client_access_token_scheme),
        session: AsyncSession = Depends(get_session),
        service: ClientService = Depends(get_client_service),
) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        client_id = get_client_id_from_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise credentials_exception

    try:
        client = service.get(session=session, pk=client_id)
    except NotFoundError:
        raise credentials_exception

    if not client.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Member is inactive",
        )

    return client


def get_current_admin(
        credentials: HTTPAuthorizationCredentials | None = Security(admin_access_token_scheme),
        session: AsyncSession = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        admin_id = get_admin_id_from_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise credentials_exception

    try:
        admin = service.get(session=session, pk=admin_id)
    except NotFoundError:
        raise credentials_exception

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Member is inactive",
        )

    return admin


def require_all(*codes: Permission):
    def dependency(
            current_admin: Admin = Depends(get_current_admin),
    ) -> Admin:
        missing = [
            code for code in codes if not admin_has_permission(current_admin, code)
        ]

        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}",
            )

        return current_admin

    return dependency


def require_permission(code: Permission):
    return require_all(code)
