from sqlalchemy.orm import Session

from src.core.security import verify_password
from src.schemas.auth_schema import TokenSchema
from src.core.exceptions import NotFoundError, UnauthorizedError, ConflictError
from src.database.models.admin import Admin
from src.repositories.admin import AdminRepository
from src.schemas.admin_schema import AdminUpdate, AdminFilter, AdminLogin
from src.services.base import BaseService


class AdminService(BaseService[Admin]):
    def __init__(self, repository: AdminRepository) -> None:
        super().__init__(repository)

    def get_all_admin_by_filters(self, session: Session, filters: AdminFilter) -> list[Admin]:
        return self.repository.get_all_admin_by_filters(session, filters)

    def login(self, session: Session, obj: AdminLogin) -> TokenSchema:
        exists_email = self.repository.get_admin_by_email(session, obj.email)

        if not exists_email:
            raise NotFoundError(detail="Phone number not exists")

        if not verify_password(obj.password, exists_email.hashed_password):
            raise UnauthorizedError(detail="Password incorrect")

        return self._issue_tokens(exists_email.id)

    def create(self, session: Session, obj: Admin) -> TokenSchema:
        exists_email = self.repository.get_admin_by_email(session, obj.email)

        if exists_email:
            raise ConflictError(detail="Phone number already exists")

        admin = self.repository.create(session, obj)
        session.commit()
        session.refresh(admin)

        return self._issue_tokens(admin.id)


    def update(self, session: Session, id: int, obj: AdminUpdate) -> Admin:
        admin = self.repository.get(session, id)

        if not admin:
            raise NotFoundError(detail="Admin not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(admin, field, value)

        updated_obj = self.repository.update(session, admin)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        admin = self.repository.get(session, id)

        if not admin:
            raise NotFoundError(detail="Admin not found")

        self.repository.delete(session, admin)