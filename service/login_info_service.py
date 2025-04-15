"""
로그인 정보 관련 비즈니스 로직
이 모듈은 로그인/로그아웃 기록 관리에 필요한 모든 비즈니스 로직을 구현합니다.
"""

from sqlalchemy.orm import Session
from model.login_info import LoginInfo
from schemas.login_info import LoginInfoCreate
from typing import List

class LoginInfoService:
    """
    로그인 정보 관리 서비스
    데이터베이스 작업과 비즈니스 로직을 처리합니다.
    """
    
    @staticmethod
    def create_login_info(db: Session, login_info: LoginInfoCreate) -> LoginInfo:
        """
        새로운 로그인/로그아웃 기록을 생성합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            login_info (LoginInfoCreate): 생성할 로그인 정보
        
        Returns:
            LoginInfo: 생성된 로그인 정보 객체
        """
        db_login_info = LoginInfo(**login_info.model_dump())
        db.add(db_login_info)
        db.commit()
        db.refresh(db_login_info)
        return db_login_info

    @staticmethod
    def get_user_login_history(db: Session, user_id: int) -> List[LoginInfo]:
        """
        특정 사용자의 로그인/로그아웃 기록을 조회합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user_id (int): 조회할 사용자의 ID
        
        Returns:
            List[LoginInfo]: 로그인/로그아웃 기록 목록
        """
        return db.query(LoginInfo).filter(LoginInfo.user_id == user_id).order_by(LoginInfo.action_time.desc()).all()
