from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenCreate(TokenBase):
    user_id: int
    access_token_expires: datetime
    refresh_token_expires: datetime

class Token(TokenBase):
    id: int
    user_id: int
    access_token_expires: datetime
    refresh_token_expires: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
