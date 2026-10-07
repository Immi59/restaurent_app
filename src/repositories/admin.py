from sqlalchemy.orm import Session
from src.database.models.admin import Admin
from src.repositories.base import BaseRepository
from src.schemas.admin_schema import AdminFilter


class AdminRepository(BaseRepository[Admin]):
    model = Admin

    def get_all_admin_by_filters(self, session: Session, filters: AdminFilter) -> list[Admin]:
        query = session.query(self.model)

        if filters.is_active is not None:
            query = query.where(self.model.is_active == filters.is_active)

        return list(session.scalars(query).all())

    def get_admin_by_email(self, session: Session, email: str) -> Admin:
        query = session.query(self.model)
        if email is not None:
            query = query.where(self.model.email == email)

        return session.scalar(query)

    def update(self, session: Session, obj: Admin) -> Admin:
        session.flush()
        return obj