from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.v1.dependancies import (
    get_manager_permission_service,
    get_manager_role_permission_service,
    get_manager_role_service,
)
from src.database.models import ManagerPermissions, ManagerRoles
from src.database.session import get_session
from src.schemas.permission_schema import (
    AssignPermissionToRole,
    PermissionBase,
    PermissionCreate,
    PermissionUpdate,
    RoleBase,
    RoleCreate,
    RoleUpdate,
)
from src.services.manager_permission import (
    ManagerPermissionService,
    ManagerRolePermissionsService,
    ManagerRoleService,
)

router = APIRouter(prefix="/manager_permissions", tags=["Manager_Permissions"])


@router.get("/role", response_model=list[RoleBase])
def get_all_role(
    session: Session = Depends(get_session),
    service: ManagerRoleService = Depends(get_manager_role_service),
):
    return service.get_all(session=session)


@router.post("/role", response_model=RoleBase)
def create_role(
    payload: RoleCreate,
    session: Session = Depends(get_session),
    service: ManagerRoleService = Depends(get_manager_role_service),
):
    obj = ManagerRoles(**payload.model_dump())
    return service.create(session=session, obj=obj)


@router.patch("/role/{role_id}", response_model=RoleBase)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    session: Session = Depends(get_session),
    service: ManagerRoleService = Depends(get_manager_role_service),
):
    return service.update(session=session, id=role_id, obj=payload)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    session: Session = Depends(get_session),
    service: ManagerRoleService = Depends(get_manager_role_service),
):
    service.delete(session=session, id=role_id)


@router.get("/", response_model=list[PermissionBase])
def get_all_permission(
    session: Session = Depends(get_session),
    service: ManagerPermissionService = Depends(get_manager_permission_service),
):
    return service.get_all(session=session)


@router.post("/", response_model=PermissionBase)
def create_permission(
    payload: PermissionCreate,
    session: Session = Depends(get_session),
    service: ManagerPermissionService = Depends(get_manager_permission_service),
):
    obj = ManagerPermissions(**payload.model_dump())
    return service.create(session=session, obj=obj)


@router.patch("/{permission_id}", response_model=PermissionBase)
def update_permission(
    permission_id: int,
    payload: PermissionUpdate,
    session: Session = Depends(get_session),
    service: ManagerPermissionService = Depends(get_manager_permission_service),
):
    return service.update(session=session, id=permission_id, obj=payload)


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int,
    session: Session = Depends(get_session),
    service: ManagerPermissionService = Depends(get_manager_permission_service),
):
    service.delete(session=session, id=permission_id)


@router.post("/assign", response_model=RoleBase)
def assign_permission_to_role(
    payload: AssignPermissionToRole,
    session: Session = Depends(get_session),
    service: ManagerRolePermissionsService = Depends(get_manager_role_permission_service),
):
    return service.assign_permission(session=session, obj=payload)


@router.post("/unassign", response_model=RoleBase)
def unassign_permission_to_role(
    payload: AssignPermissionToRole,
    session: Session = Depends(get_session),
    service: ManagerRolePermissionsService = Depends(get_manager_role_permission_service),
):
    return service.unassign_permission(session=session, obj=payload)