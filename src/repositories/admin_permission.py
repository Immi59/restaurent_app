from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.admin_role import AdminRolePermissions, AdminRoles, AdminPermissions
from src.repositories.base import BaseRepository


class AdminRoleRepository(BaseRepository[AdminRoles]):
    model = AdminRoles

    def update(self, session: Session, obj: AdminRoles) -> AdminRoles:
        session.flush()
        return obj


class AdminRolePermissionsRepository(BaseRepository[AdminRolePermissions]):
    model = AdminRolePermissions

    def delete(self, session: Session, obj: AdminRolePermissions) -> None:
        stmt = select(AdminRolePermissions).where(
            AdminRolePermissions.role_id == obj.role_id,
            AdminRolePermissions.permission_id == obj.permission_id,
        )

        assign_obj = session.scalar(stmt)

        if assign_obj is None:
            raise NotFoundError("Permission is not assigned to this role")
        session.delete(assign_obj)

class AdminPermissionRepository(BaseRepository[AdminPermissions]):
    model = AdminPermissions

    def update(self, session: Session, obj: AdminPermissions) -> AdminPermissions:
        session.flush()
        return obj