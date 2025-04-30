from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CodeDetailBase(BaseModel):
    name: str
    value: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[str] = None
    is_active: bool = True
    icon: Optional[str] = None


class CodeDetailCreate(CodeDetailBase):
    id: str
    group_id: str


class CodeDetailUpdate(CodeDetailBase):
    pass


class CodeDetail(CodeDetailBase):
    id: str
    group_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CodeGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class CodeGroupCreate(CodeGroupBase):
    id: str = Field(..., description="그룹 코드 ID (예: G001)")


class CodeGroupUpdate(CodeGroupBase):
    pass


class CodeGroup(CodeGroupBase):
    id: str
    created_at: datetime
    updated_at: datetime
    details: List[CodeDetail] = []

    class Config:
        orm_mode = True
