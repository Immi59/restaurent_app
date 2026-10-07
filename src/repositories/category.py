from sqlalchemy.orm import Session

from src.database.models.category import Category
from src.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category

    def update(self, session: Session, obj: Category) -> Category:
        session.flush()
        return obj