from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.admin_role import AdminRoles, AdminPermissions, AdminRolePermissions
from src.repositories.admin_permission import AdminRoleRepository,AdminPermissionRepository,AdminRolePermissionsRepository
from src.schemas.permission_schema import RoleUpdate, PermissionUpdate, AssignPermissionToRole
from src.services.base import BaseService


class AdminRoleService(BaseService[AdminRoles]):
    def __init__(self, admin_role_repo: AdminRoleRepository) -> None:
        self.admin_role_repo = admin_role_repo
        super().__init__(admin_role_repo)

    def update(self, session: Session, id: int, obj: RoleUpdate) -> AdminRoles:
        role = self.repository.get(session, id)

        if not role:
            raise NotFoundError(detail="Admin role not found")

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
            raise NotFoundError(detail="Admin role not found")

        self.repository.delete(session, role)


class AdminPermissionService(BaseService[AdminPermissions]):
    def __init__(self, admin_permission_repo: AdminPermissionRepository) -> None:
        self.admin_permission_repo = admin_permission_repo
        super().__init__(admin_permission_repo)

    def update(self, session: Session, id: int, obj: PermissionUpdate) -> AdminPermissions:
        permission = self.repository.get(session, id)

        if not permission:
            raise NotFoundError(detail="Admin permission not found")

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
            raise NotFoundError(detail="Admin permission not found")

        self.repository.delete(session, permission)


class AdminRolePermissionsService(BaseService):
    def __init__(
        self,
        admin_role_repo: AdminRoleRepository,
        admin_role_permission_repo: AdminRolePermissionsRepository,
    ) -> None:
        self.admin_role_repo = admin_role_repo
        self.admin_role_permission_repo = admin_role_permission_repo
        super().__init__(admin_role_permission_repo)

    def assign_permission(self, session: Session, obj: AssignPermissionToRole) -> AdminRoles:
        role = self.admin_role_repo.get(session, obj.role_id)
        if not role:
            raise NotFoundError(detail="Admin role not found")

        assign_obj = AdminRolePermissions(**obj.model_dump(exclude_unset=True))

        self.admin_role_permission_repo.create(session, assign_obj)
        session.commit()
        return role

    def unassign_permission(self, session: Session, obj: AssignPermissionToRole) -> AdminRoles:
        role = self.admin_role_repo.get(session, obj.role_id)
        if not role:
            raise NotFoundError(detail="Admin role not found")

        assign_obj = AdminRolePermissions(**obj.model_dump(exclude_unset=True))

        self.admin_role_permission_repo.delete(session, assign_obj)
        session.commit()
        return role