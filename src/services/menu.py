from sqlalchemy.orm import Session

from src.services.base import ModelType
from src.database.models import Category
from src.core.exceptions import NotFoundError
from src.database.models.menu import Menu
from src.repositories.menu import MenuRepository
from src.repositories.category import CategoryRepository
from src.schemas.menu_schema import MenuUpdate, MenuCreate, MenuFilter
from src.services.base import BaseService


class MenuService(BaseService[Menu]):
    def __init__(self, menu_repo: MenuRepository, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo
        self.menu_repo = menu_repo
        super().__init__(menu_repo)

    def get_all_menu_by_filters(self, session: Session, filters: MenuFilter) -> list[Menu]:
        return self.menu_repo.get_all_menu_by_filters(session, filters)

    def create(self, session: Session, obj: MenuCreate) -> MenuCreate:
        category = self.category_repo.get(session, obj.category_id)

        if not category:
            raise NotFoundError(detail="Category not found")

        return self.menu_repo.create(session, obj)

    def update(self, session: Session, id: int, obj: MenuUpdate) -> Menu:
        menu = self.repository.get(session, id)

        if not menu:
            raise NotFoundError(detail="Menu not found")

        update_data = obj.model_dump(exclude_unset=True)

        if "category_id" in update_data:
            category = session.query(Category).filter(Category.id == update_data["category_id"]).first()
            if not category:
                raise NotFoundError(detail="Category not found")

        for field, value in update_data.items():
            setattr(menu, field, value)

        updated_obj = self.repository.update(session, menu)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        menu = self.repository.get(session, id)

        if not menu:
            raise NotFoundError(detail="Menu not found")

        self.repository.delete(session, menu)
