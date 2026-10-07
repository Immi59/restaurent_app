from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class AdminRolePermissions(Base):
    __tablename__ = "admin_role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("admin_roles.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("admin_permissions.id", ondelete="CASCADE"), primary_key=True
    )


class AdminRole(Base):
    __tablename__ = "admin_role"

    # Если таблица админов называется "admins" (во множественном числе), укажите "admins.id"
    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admins.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("admin_roles.id", ondelete="CASCADE"), primary_key=True
    )
    granted_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


class AdminRoles(Base):
    __tablename__ = "admin_roles"
    """admin, support, superadmin"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), default=None)

    permissions: Mapped[list["AdminPermissions"]] = relationship(
        secondary=AdminRolePermissions.__table__,
        lazy="selectin",
    )


class AdminPermissions(Base):
    __tablename__ = "admin_permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(String(255), default=None)