"""
사용자 데이터베이스 모델 정의
이 모듈은 사용자 테이블의 구조와 기본 설정을 정의합니다.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
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

class User(Base):
    """
    사용자 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (int): 사용자 고유 식별자 (기본키)
        username (str): 사용자 이름 (고유값)
        email (str): 이메일 주소 (고유값)
        created_at (str): 계정 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 정보 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = "users"  # 테이블 이름

    # 컬럼 정의
    id = Column(Integer, primary_key=True, index=True)  # 기본키
    username = Column(String, unique=True, index=True)  # 사용자 이름 (유니크 인덱스)
    email = Column(String, unique=True, index=True)     # 이메일 (유니크 인덱스)
    created_at = Column(String, default=get_current_time)  # 생성 시간
    updated_at = Column(String, default=get_current_time, onupdate=get_current_time)  # 수정 시간

    # 관계 정의
    login_history = relationship("LoginInfo", back_populates="user")
