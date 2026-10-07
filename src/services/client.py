from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError, ConflictError, UnauthorizedError
from src.core.security import verify_password
from src.database.models.client import Client
from src.repositories.client import ClientRepository
from src.schemas.auth_schema import TokenSchema
from src.schemas.client_schema import ClientUpdate, ClientFilter, ClientLogin
from src.services.base import BaseService


class ClientService(BaseService[Client]):
    def __init__(self, repository: ClientRepository) -> None:
        super().__init__(repository)

    def login(self, session: Session, obj: ClientLogin) -> TokenSchema:
        exists_phone_number = self.repository.get_user_by_phone_number(session, obj.phone_number)

        if not exists_phone_number:
            raise NotFoundError(detail="Phone number not exists")

        if not verify_password(obj.password, exists_phone_number.hashed_password):
            raise UnauthorizedError(detail="Password incorrect")

        return self._issue_tokens(exists_phone_number.id)

    def create(self, session: Session, obj: Client) -> TokenSchema:
        exists_phone_number = self.repository.get_user_by_phone_number(session, obj.phone_number)

        if exists_phone_number:
            raise ConflictError(detail="Phone number already exists")

        client = self.repository.create(session, obj)
        session.commit()
        session.refresh(client)

        return self._issue_tokens(client.id)

    def get_all_client_by_filters(self, session: Session, filters: ClientFilter) -> Client:
        return self.repository.get_all_client_by_filters(session, filters)

    def update(self, session: Session, id: int, obj: ClientUpdate) -> Client:
        client = self.repository.get(session, id)

        if not client:
            raise NotFoundError(detail="Client not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(client, field, value)

        updated_obj = self.repository.update(session, client)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        client = self.repository.get(session, id)

        if not client:
            raise NotFoundError(detail="Client not found")

        self.repository.delete(session, client)
