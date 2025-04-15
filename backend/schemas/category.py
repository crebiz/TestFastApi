from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    fund: Optional[float] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None
    fund: Optional[float] = None

class Category(CategoryBase):
    id: str
    name: str
    parent_id: Optional[str] = None
    fund: Optional[float] = None
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
        from_attributes = True