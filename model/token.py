from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.database import Base
from datetime import datetime

def get_current_time():
    """
    현재 시간을 'yyyymmddhhmmss' 형식의 문자열로 반환
    
    Returns:
        str: 'yyyymmddhhmmss' 형식의 현재 시간 (예: '20250326123456')
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  
    access_token = Column(String)
    refresh_token = Column(String)
    access_token_expires = Column(DateTime)
    refresh_token_expires = Column(DateTime)
    created_at = Column(String, default=get_current_time)  # 생성 시간
    updated_at = Column(String, default=get_current_time, onupdate=get_current_time)  # 수정 시간
