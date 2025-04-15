"""
로그인 정보 데이터베이스 모델 정의
이 모듈은 사용자의 로그인/로그아웃 기록을 저장하는 테이블의 구조를 정의합니다.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
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

class LoginInfo(Base):
    """
    로그인 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (int): 로그 고유 식별자 (기본키)
        user_id (int): 사용자 ID (외래키)
        action_type (str): 액션 타입 ('login' 또는 'logout')
        created_at (str): 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = "login_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action_type = Column(String)  # 'login' 또는 'logout'
    created_at = Column(String, default=get_current_time)  # 생성 시간
    updated_at = Column(String, default=get_current_time, onupdate=get_current_time)  # 수정 시간

    # 관계 설정
    user = relationship("User", back_populates="login_history")
