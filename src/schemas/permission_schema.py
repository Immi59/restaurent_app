from datetime import datetime

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    id: int
    name: str
    description: str | None
    permissions: list["PermissionBase"] | None = Field(None)


class RoleCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    description: str | None = Field(None, max_length=100)


class RoleUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, max_length=100)


class PermissionBase(BaseModel):
    id: int
    code: str
    description: str | None


class PermissionCreate(BaseModel):
    code: str = Field(min_length=3, max_length=20)
    description: str | None = Field(None, max_length=100)


class PermissionUpdate(BaseModel):
    code: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, max_length=100)


class AssignPermissionToRole(BaseModel):
    role_id: int
    permission_id: int