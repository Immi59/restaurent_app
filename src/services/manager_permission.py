from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.manager_role import (
    ManagerPermissions,
    ManagerRolePermissions,
    ManagerRoles,
)
from src.repositories.manager_permission import (
    ManagerPermissionRepository,
    ManagerRolePermissionsRepository,
    ManagerRoleRepository,
)
from src.schemas.permission_schema import (
    AssignPermissionToRole,
    PermissionUpdate,
    RoleUpdate,
)
from src.services.base import BaseService


class ManagerRoleService(BaseService[ManagerRoles]):
    def __init__(self, manager_role_repo: ManagerRoleRepository) -> None:
        self.manager_role_repo = manager_role_repo
        super().__init__(manager_role_repo)

    def update(self, session: Session, id: int, obj: RoleUpdate) -> ManagerRoles:
        role = self.repository.get(session, id)

        if not role:
            raise NotFoundError(detail="Manager role not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(role, field, value)

        updated_obj = self.repository.update(session, role)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        role = self.repository.get(session, id)

        if not role:
            raise NotFoundError(detail="Manager role not found")

        self.repository.delete(session, role)


class ManagerPermissionService(BaseService[ManagerPermissions]):
    def __init__(self, manager_permission_repo: ManagerPermissionRepository) -> None:
        self.manager_permission_repo = manager_permission_repo
        super().__init__(manager_permission_repo)

    def update(self, session: Session, id: int, obj: PermissionUpdate) -> ManagerPermissions:
        permission = self.repository.get(session, id)

        if not permission:
            raise NotFoundError(detail="Manager permission not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(permission, field, value)

        updated_obj = self.repository.update(session, permission)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        permission = self.repository.get(session, id)

        if not permission:
            raise NotFoundError(detail="Manager permission not found")

        self.repository.delete(session, permission)


class ManagerRolePermissionsService(BaseService):
    def __init__(
        self,
        manager_role_repo: ManagerRoleRepository,
        manager_role_permission_repo: ManagerRolePermissionsRepository,
    ) -> None:
        self.manager_role_repo = manager_role_repo
        self.manager_role_permission_repo = manager_role_permission_repo
        super().__init__(manager_role_permission_repo)

    def assign_permission(self, session: Session, obj: AssignPermissionToRole) -> ManagerRoles:
        role = self.manager_role_repo.get(session, obj.role_id)
        if not role:
            raise NotFoundError(detail="Manager role not found")

        assign_obj = ManagerRolePermissions(**obj.model_dump(exclude_unset=True))

        self.manager_role_permission_repo.create(session, assign_obj)
        session.commit()
        return role

    def unassign_permission(self, session: Session, obj: AssignPermissionToRole) -> ManagerRoles:
        role = self.manager_role_repo.get(session, obj.role_id)
        if not role:
            raise NotFoundError(detail="Manager role not found")

        assign_obj = ManagerRolePermissions(**obj.model_dump(exclude_unset=True))

        self.manager_role_permission_repo.delete(session, assign_obj)
        session.commit()
        return role