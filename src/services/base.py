from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.core.security import create_access_token, create_refresh_token
from src.database.base import Base
from src.repositories.base import BaseRepository
from src.schemas.auth_schema import TokenSchema

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        self.repository = repository

    @staticmethod
    def _issue_tokens(user_id: int) -> TokenSchema:
        return TokenSchema.model_validate(
            {
                "access_token": create_access_token(user_id),
                "refresh_token": create_refresh_token(user_id),
                "token_type": "bearer",
            }
        )

    def get(self, session: Session, pk: int) -> ModelType | None:
        db_obj = self.repository.get(session, pk)
        if not db_obj:
            raise NotFoundError(detail="Not found")
        return self.repository.get(session, pk)

    def get_all(self, session: Session) -> list[ModelType]:
        return self.repository.get_all(session)

    def create(self, session: Session, obj: ModelType) -> ModelType:
        return self.repository.create(session, obj)

    def update(self, session: Session, obj: ModelType) -> ModelType:
        return self.repository.update(session, obj)

    def delete(self, session: Session, obj: ModelType) -> None:
        self.repository.delete(session, obj)
