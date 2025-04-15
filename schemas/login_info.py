"""
로그인 정보 스키마 정의
이 모듈은 로그인 정보의 데이터 검증과 직렬화를 위한 Pydantic 모델을 정의합니다.
"""

from pydantic import BaseModel

class LoginInfoBase(BaseModel):
    """로그인 정보의 기본 스키마"""
    user_id: int
    action_type: str

class LoginInfoCreate(LoginInfoBase):
    """로그인 정보 생성 스키마"""
    pass

class LoginInfo(LoginInfoBase):
    """로그인 정보 응답 스키마"""
    id: int
    action_time: str

    class Config:
        """Pydantic 설정"""
        from_attributes = True
