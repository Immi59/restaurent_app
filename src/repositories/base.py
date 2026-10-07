from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from src.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def get(self, session: Session, pk: int) -> ModelType | None:
        return session.get(self.model, pk)

    def get_all(self, session: Session) -> list[ModelType]:
        return list(session.query(self.model).all())

    def create(self, session: Session, obj: ModelType) -> ModelType:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def update(self, session: Session, obj: ModelType) -> ModelType:
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, obj: ModelType) -> None:
        session.delete(obj)
        session.commit()
