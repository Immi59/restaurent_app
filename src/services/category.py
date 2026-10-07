from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.category import Category
from src.repositories.category import CategoryRepository
from src.schemas.category_schema import CategoryUpdate
from src.services.base import BaseService


class CategoryService(BaseService[Category]):
    def __init__(self, repository: CategoryRepository) -> None:
        super().__init__(repository)

    def update(self, session: Session, id: int, obj: CategoryUpdate) -> Category:
        category = self.repository.get(session, id)

        if not category:
            raise NotFoundError(detail="Category not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(category, field, value)

        updated_obj = self.repository.update(session, category)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        category = self.repository.get(session, id)

        if not category:
            raise NotFoundError(detail="Category not found")

        self.repository.delete(session, category)