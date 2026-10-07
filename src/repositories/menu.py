from sqlalchemy.orm import Session

from src.schemas.menu_schema import MenuFilter
from src.database.models.menu import Menu
from src.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    model = Menu

    def get_all_menu_by_filters(self, session: Session, filters: MenuFilter) -> list[Menu]:
        query = session.query(self.model)
        if filters.category_id is not None:
            query = query.where(self.model.category_id == filters.category_id)

        if filters.is_active is not None:
            query = query.where(self.model.is_active == filters.is_active)

        return list(session.scalars(query).all())

    def update(self, session: Session, obj: Menu) -> Menu:
        session.flush()
        return obj



'''
menu = 1, 2, 3, 4, 5
is_active false = 1, 3
category_id 2 = 1, 2, 3
category_id 1 = 4, 5


request param = category_id=2, is_active=False

menu = 1, 2, 3
response menu = 2

'''