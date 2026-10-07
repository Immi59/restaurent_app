from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.manager_role import ManagerRolePermissions, ManagerRoles, ManagerPermissions
from src.repositories.base import BaseRepository


class ManagerRoleRepository(BaseRepository[ManagerRoles]):
    model = ManagerRoles

    def update(self, session: Session, obj: ManagerRoles) -> ManagerRoles:
        session.flush()
        return obj


class ManagerRolePermissionsRepository(BaseRepository[ManagerRolePermissions]):
    model = ManagerRolePermissions

    def delete(self, session: Session, obj: ManagerRolePermissions) -> None:
        stmt = select(ManagerRolePermissions).where(
            ManagerRolePermissions.role_id == obj.role_id,
            ManagerRolePermissions.permission_id == obj.permission_id,
        )

        assign_obj = session.scalar(stmt)

        if assign_obj is None:
            raise NotFoundError("Permission is not assigned to this role")
        session.delete(assign_obj)


class ManagerPermissionRepository(BaseRepository[ManagerPermissions]):
    model = ManagerPermissions

    def update(self, session: Session, obj: ManagerPermissions) -> ManagerPermissions:
        session.flush()
        return obj
