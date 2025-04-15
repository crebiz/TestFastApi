"""
사용자 관련 Pydantic 모델 정의
이 모듈은 API 요청/응답에 사용되는 데이터 검증 및 직렬화 스키마를 정의합니다.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    사용자 기본 정보 스키마
    모든 사용자 관련 스키마의 기본이 되는 클래스입니다.
    
    Attributes:
        username (str): 사용자 이름
        email (str): 이메일 주소
    """
    username: str
    email: str

class UserCreate(UserBase):
    """
    사용자 생성 요청 스키마
    UserBase를 상속받아 사용자 생성에 필요한 필드만 정의합니다.
    """
    pass

class UserUpdate(BaseModel):
    """
    사용자 정보 수정 요청 스키마
    모든 필드가 선택적(Optional)이어서 부분 업데이트가 가능합니다.
    
    Attributes:
        username (Optional[str]): 변경할 사용자 이름 (선택)
        email (Optional[str]): 변경할 이메일 주소 (선택)
    """
    username: Optional[str] = None
    email: Optional[str] = None

class User(UserBase):
    """
    사용자 정보 응답 스키마
    데이터베이스에서 조회한 사용자 정보를 반환할 때 사용됩니다.
    
    Attributes:
        id (int): 사용자 고유 식별자
        created_at (str): 계정 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 정보 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    id: int
    created_at: str
    updated_at: str

    class Config:
        """Pydantic 설정"""
        from_attributes = True  # ORM 모델을 Pydantic 모델로 변환 허용
