from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    id: int
    name: str
    created_at: datetime


class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class CategoryUpdate(CategoryCreate):
    pass