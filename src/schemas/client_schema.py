from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

#


class ClientBase(BaseModel):
    id: int
    full_name: str
    phone_number: str
    is_active: bool
    created_at: datetime


class ClientCreate(BaseModel):
    full_name: str = Field(min_length=5, max_length=50)
    phone_number: str
    password: str


class ClientLogin(BaseModel):
    phone_number: str
    password: str


class ClientUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=5, max_length=50)
    phone_number: str | None = Field(None)
    is_active: bool | None = Field(None)


class ClientFilter(BaseModel):
    is_active: bool = Field(True)
