from datetime import datetime

from pydantic import BaseModel, Field



class MenuBase(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    is_active: bool
    category_id: int
    created_at: datetime



class MenuCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: str | None = Field(None, max_length=500)
    price: int = Field(..., gt=0)
    image_url: str | None = None
    is_active: bool = True
    category_id: int  # Внешний ключ передается клиентом при создании


class MenuUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    description: str | None = Field(None, max_length=500)
    price: int | None = Field(None, gt=0)
    image_url: str | None = None
    is_active: bool | None = None
    category_id: int | None = None


class MenuFilter(BaseModel):
    is_active: bool = Field(True)
    category_id: int | None = Field(None)
