"""
사용자 관련 비즈니스 로직
이 모듈은 사용자 관리에 필요한 모든 비즈니스 로직을 구현합니다.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.user import User
from schemas.user import UserCreate, UserUpdate
from typing import List, Optional

class UserService:
    """
    사용자 관리 서비스
    데이터베이스 작업과 비즈니스 로직을 처리합니다.
    """
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        새로운 사용자를 생성합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user (UserCreate): 생성할 사용자 정보
        
        Returns:
            User: 생성된 사용자 객체
        
        Raises:
            HTTPException: 이메일이 이미 등록된 경우 발생
        """
        # 이메일 중복 검사
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
        
        # 새 사용자 생성
        db_user = User(username=user.username, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        사용자 목록을 조회합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            skip (int): 건너뛸 레코드 수
            limit (int): 조회할 최대 레코드 수
        
        Returns:
            List[User]: 사용자 목록
        """
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """
        특정 사용자의 정보를 조회합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user_id (int): 조회할 사용자의 ID
        
        Returns:
            User: 사용자 객체
        
        Raises:
            HTTPException: 사용자를 찾을 수 없는 경우 발생
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        이메일로 사용자를 조회합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            email (str): 조회할 사용자의 이메일
            
        Returns:
            Optional[User]: 찾은 사용자 객체 또는 None
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
        """
        사용자 정보를 수정합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user_id (int): 수정할 사용자의 ID
            user (UserUpdate): 수정할 정보
        
        Returns:
            User: 수정된 사용자 객체
        
        Raises:
            HTTPException: 사용자를 찾을 수 없는 경우 발생
        """
        # 사용자 존재 확인
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        # 제공된 필드만 업데이트
        for var, value in vars(user).items():
            if value is not None:
                setattr(db_user, var, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        """
        사용자를 삭제합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user_id (int): 삭제할 사용자의 ID
        
        Returns:
            dict: 삭제 성공 메시지
        
        Raises:
            HTTPException: 사용자를 찾을 수 없는 경우 발생
        """
        # 사용자 존재 확인
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        # 사용자 삭제
        db.delete(db_user)
        db.commit()
        return {"message": "사용자가 삭제되었습니다"}
