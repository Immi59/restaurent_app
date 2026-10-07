from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.manager import Manager
from src.repositories.manager import ManagerRepository
from src.schemas.manager_schema import ManagerUpdate
from src.services.base import BaseService


class ManagerService(BaseService[Manager]):
    def __init__(self, repository: ManagerRepository) -> None:
        super().__init__(repository)

    def update(self, session: Session, id: int, obj: ManagerUpdate) -> Manager:
        manager = self.repository.get(session, id)

        if not manager:
            raise NotFoundError(detail="Admin not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(manager, field, value)

        updated_obj = self.repository.update(session, manager)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        manager = self.repository.get(session, id)

        if not manager:
            raise NotFoundError(detail="Admin not found")

        self.repository.delete(session, manager)