"""
카테고리 데이터베이스 모델 정의
이 모듈은 카테고리 테이블의 구조와 기본 설정을 정의합니다.
"""

from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime


def get_current_time():
    """
    현재 시간을 'yyyymmddhhmmss' 형식의 문자열로 반환
    
    Returns:
        str: 'yyyymmddhhmmss' 형식의 현재 시간 (예: '20250326123456')
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')


class Category(Base):
    """
    카테고리 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (str): 카테고리 고유 식별자 (기본키)
        name (str): 카테고리 이름
        parent_id (str): 상위 카테고리 ID
        fund (Numeric): 카테고리 자금 (기본값 0)
        created_at (str): 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = 'category'

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(String(255), nullable=True)  
    fund = Column(Numeric, default=0)
    created_at = Column(String, default=get_current_time)  
    updated_at = Column(String, default=get_current_time, onupdate=get_current_time)  

    def __repr__(self):
        return f"<Category(id='{self.id}', name='{self.name}', parent_id='{self.parent_id}', fund={self.fund}, created_at='{self.created_at}', updated_at='{self.updated_at}')>"
