from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class ManagerRolePermissions(Base):
    __tablename__ = "manager_role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("manager_roles.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("manager_permissions.id", ondelete="CASCADE"), primary_key=True
    )


class ManagerRole(Base):
    __tablename__ = "manager_role"

    manager_id: Mapped[int] = mapped_column(
        ForeignKey("managers.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("manager_roles.id", ondelete="CASCADE"), primary_key=True
    )
    granted_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


class ManagerRoles(Base):
    __tablename__ = "manager_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), default=None)

    permissions: Mapped[list["ManagerPermissions"]] = relationship(
        secondary=ManagerRolePermissions.__table__,
        lazy="selectin",
    )


class ManagerPermissions(Base):
    __tablename__ = "manager_permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), default=None)