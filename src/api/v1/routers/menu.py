from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.models import Menu
from src.schemas.menu_schema import MenuCreate, MenuBase, MenuUpdate, MenuFilter
from src.api.v1.dependancies import get_menu_service
from src.services.menu import MenuService
from src.database.session import get_session

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.get("/", response_model=list[MenuBase])
def get_all_menus(
        filters: MenuFilter = Query(None),
        session: Session = Depends(get_session),
        service: MenuService = Depends(get_menu_service),
):
    return service.get_all_menu_by_filters(session=session, filters=filters)


@router.post("/", response_model=MenuBase, status_code=status.HTTP_201_CREATED)
def create_menu(
        payload: MenuCreate,
        session: Session = Depends(get_session),
        service: MenuService = Depends(get_menu_service),
):

    payload_dump = payload.model_dump()
    db_menu = Menu(**payload_dump)
    new_menu = service.create(session=session, obj=db_menu)
    return new_menu


@router.get("/{menu_id}", response_model=MenuBase, status_code=status.HTTP_200_OK)
def get_menu_by_id(
        menu_id: int,
        session: Session = Depends(get_session),
        service: MenuService = Depends(get_menu_service),
):
    return service.get(session, menu_id)


@router.patch("/{menu_id}", response_model=MenuBase, status_code=status.HTTP_200_OK)
def update_menu(
        payload: MenuUpdate,
        menu_id: int,
        session: Session = Depends(get_session),
        service: MenuService = Depends(get_menu_service),
):
    return service.update(session, menu_id, payload)


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
        menu_id: int,
        session: Session = Depends(get_session),
        service: MenuService = Depends(get_menu_service),
):
    return service.delete(session, menu_id)  # noqa