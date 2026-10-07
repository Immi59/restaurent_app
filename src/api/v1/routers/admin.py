from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.schemas.auth_schema import TokenSchema
from src.core.security import hash_password
from src.database.models import Admin
from src.schemas.admin_schema import AdminCreate, AdminBase, AdminUpdate, AdminFilter, AdminLogin
from src.api.v1.dependancies import get_admin_service, get_current_admin
from src.services.admin import AdminService
from src.database.session import get_session

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/", response_model=list[AdminBase])
def get_all_admins(
        filters: AdminFilter = Query(None),
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.get_all_admin_by_filters(session=session, filters=filters)


@router.post("/registration", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
def create_admin(
        payload: AdminCreate,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    payload_dump = payload.model_dump()
    hashed_password = hash_password(payload_dump.get("password"))
    payload_dump["hashed_password"] = hashed_password
    payload_dump.pop("password")
    db_admin = Admin(**payload_dump)
    new_admin = service.create(session=session, obj=db_admin)
    return new_admin

@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
def login_client(
        payload: AdminLogin,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.login(session=session, obj=payload)

@router.get("/me", response_model=AdminBase, status_code=status.HTTP_200_OK)
def get_client_me(
        current_admin: Admin = Depends(get_current_admin),
):
    return current_admin


@router.get("/{admin_id}", response_model=AdminBase, status_code=status.HTTP_200_OK)
def get_admin_by_id(
        admin_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.get(session, admin_id)


@router.patch("/{admin_id}", response_model=AdminBase, status_code=status.HTTP_200_OK)
def update_admin(
        payload: AdminUpdate,
        admin_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):

    return service.update(session, admin_id, payload)


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
        admin_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.delete(session, admin_id)  # noqa