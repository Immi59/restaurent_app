from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.database.models import Client
from src.schemas.auth_schema import TokenSchema
from src.schemas.client_schema import ClientCreate, ClientBase, ClientUpdate, ClientFilter, ClientLogin
from src.api.v1.dependancies import get_client_service, get_current_client
from src.services.client import ClientService
from src.database.session import get_session

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientBase])
def get_all_clients(
        filters: ClientFilter = Query(None),
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.get_all_client_by_filters(session=session, filters=filters)


@router.post("/registration", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
def create_client(
        payload: ClientCreate,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    payload_dump = payload.model_dump()
    hashed_password = hash_password(payload_dump.get("password"))
    payload_dump["hashed_password"] = hashed_password
    payload_dump.pop("password")
    db_client = Client(**payload_dump)
    return service.create(session=session, obj=db_client)


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
def login_client(
        payload: ClientLogin,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.login(session=session, obj=payload)


@router.get("/me", response_model=ClientBase, status_code=status.HTTP_200_OK)
def get_client_me(
        current_client: Client = Depends(get_current_client),
):
    return current_client


@router.get("/{client_id}", response_model=ClientBase, status_code=status.HTTP_200_OK)
def get_client_by_id(
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.get(session, client_id)


@router.patch("/{client_id}", response_model=ClientBase, status_code=status.HTTP_200_OK)
def update_client(
        payload: ClientUpdate,
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.update(session, client_id, payload)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.delete(session, client_id)  # noqa
