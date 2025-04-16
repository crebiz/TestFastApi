from typing import Optional
from pydantic import BaseModel


class FundBase(BaseModel):
    financial_comp: str
    type: str
    account_num: str
    fund_nm: str

class FundCreate(FundBase):
    pass

class FundUpdate(BaseModel):
    financial_comp: Optional[str] = None
    type: Optional[str] = None
    account_num: Optional[str] = None

class Fund(FundBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        orm_mode = True