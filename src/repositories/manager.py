from sqlalchemy.orm import Session
from src.database.models.manager import Manager
from src.repositories.base import BaseRepository


class ManagerRepository(BaseRepository[Manager]):
    model = Manager

    def update(self, session: Session, obj: Manager) -> Manager:
        session.flush()
        return obj