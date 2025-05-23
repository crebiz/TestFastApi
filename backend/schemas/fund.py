from typing import Optional
from pydantic import BaseModel


class FundBase(BaseModel):
    financial_comp: str
    type: str
    account_num: str
    fund_nm: str
    state: str
    invest_type: Optional[str] = None
    note: Optional[str] = None

class FundCreate(FundBase):
    pass

class FundUpdate(BaseModel):
    financial_comp: Optional[str] = None
    type: Optional[str] = None
    account_num: Optional[str] = None
    fund_nm: Optional[str] = None
    state: Optional[str] = None
    invest_type: Optional[str] = None
    note: Optional[str] = None

class Fund(FundBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        orm_mode = True