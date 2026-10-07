from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class AdminBase(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class AdminCreate(BaseModel):
    full_name: str = Field(min_length=5, max_length=50)
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email : str
    password: str


class AdminUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=5, max_length=50)
    email: EmailStr | None = Field(None)
    is_active: bool | None = Field(None)


class AdminFilter(BaseModel):
    is_active: bool = Field(True)