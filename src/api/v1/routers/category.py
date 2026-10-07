from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Category
from src.schemas.category_schema import CategoryCreate, CategoryBase, CategoryUpdate
from src.api.v1.dependancies import get_category_service
from src.services.category import CategoryService
from src.database.session import get_session

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryBase])
def get_all_categories(
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return service.get_all(session=session)


@router.post("/", response_model=CategoryBase, status_code=status.HTTP_201_CREATED)
def create_category(
        payload: CategoryCreate,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    db_category = Category(**payload.model_dump())
    new_category = service.create(session=session, obj=db_category)
    return new_category


@router.get("/{category_id}", response_model=CategoryBase, status_code=status.HTTP_200_OK)
def get_category_by_id(
        category_id: int,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return service.get(session, category_id)


@router.put("/{category_id}", response_model=CategoryBase, status_code=status.HTTP_200_OK)
def update_category(
        payload: CategoryUpdate,
        category_id: int,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):

    return service.update(session, category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return service.delete(session, category_id)  # noqa


