from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class ManagerBase(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class ManagerCreate(BaseModel):
    full_name: str = Field(min_length=5, max_length=50)
    email: EmailStr
    phone_number: str
    password: str

class ManagerUpdate(ManagerCreate):
        pass

class ManagerFilter(BaseModel):
    is_active: bool = Field(True)
    category_id: int | None = Field(None)