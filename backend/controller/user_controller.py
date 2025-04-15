"""
사용자 관련 API 엔드포인트 정의
이 모듈은 사용자 관리를 위한 RESTful API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.database.database import get_db
from backend.service.user_service import UserService
from backend.service.login_info_service import LoginInfoService
from backend.service.token_service import TokenService
from backend.schemas.user import User, UserCreate, UserUpdate
from backend.schemas.login_info import LoginInfoCreate, LoginInfo
from backend.middleware.auth import jwt_bearer

# API 라우터 설정
router = APIRouter(
    prefix="/users",  # URL 접두사
    tags=["users"]    # Swagger 문서 태그
)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 생성합니다.
    
    Args:
        user (UserCreate): 생성할 사용자 정보
        db (Session): 데이터베이스 세션
    
    Returns:
        User: 생성된 사용자 정보
    
    Raises:
        HTTPException: 이메일이 이미 등록된 경우 400 에러
    """
    return UserService.create_user(db=db, user=user)

@router.get("/", response_model=List[User], dependencies=[Depends(jwt_bearer)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    사용자 목록을 조회합니다.
    
    Args:
        skip (int): 건너뛸 레코드 수 (기본값: 0)
        limit (int): 조회할 최대 레코드 수 (기본값: 100)
        db (Session): 데이터베이스 세션
    
    Returns:
        List[User]: 사용자 목록
    """
    return UserService.get_users(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User, dependencies=[Depends(jwt_bearer)])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자의 정보를 조회합니다.
    
    Args:
        user_id (int): 조회할 사용자의 ID
        db (Session): 데이터베이스 세션
    
    Returns:
        User: 사용자 정보
    
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우 404 에러
    """
    return UserService.get_user(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=User, dependencies=[Depends(jwt_bearer)])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    사용자 정보를 수정합니다.
    
    Args:
        user_id (int): 수정할 사용자의 ID
        user (UserUpdate): 수정할 정보
        db (Session): 데이터베이스 세션
    
    Returns:
        User: 수정된 사용자 정보
    
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우 404 에러
    """
    return UserService.update_user(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", dependencies=[Depends(jwt_bearer)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    사용자를 삭제합니다.
    
    Args:
        user_id (int): 삭제할 사용자의 ID
        db (Session): 데이터베이스 세션
    
    Returns:
        dict: 삭제 성공 메시지
    
    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우 404 에러
    """
    return UserService.delete_user(db=db, user_id=user_id)

@router.post("/google-login")
async def google_login(user_data: Dict, db: Session = Depends(get_db)):
    """
    구글 로그인 정보를 저장하고 JWT 토큰을 발급합니다.
    
    Args:
        user_data (Dict): 구글 로그인에서 받은 사용자 정보
        db (Session): 데이터베이스 세션
    
    Returns:
        Dict: 사용자 정보와 JWT 토큰
    """
    print("Received user_data:", user_data)  # 디버깅 로그 추가
    
    user = UserCreate(
        username=user_data["name"],
        email=user_data["email"]
    )
    
    # 기존 사용자 확인
    existing_user = UserService.get_user_by_email(db=db, email=user.email)
    
    if existing_user:
        print("Found existing user:", existing_user)  # 디버깅 로그 추가
        # 로그인 기록 저장
        login_info = LoginInfoCreate(user_id=existing_user.id, action_type="login")
        LoginInfoService.create_login_info(db=db, login_info=login_info)
        
        # JWT 토큰 생성
        tokens = TokenService.create_tokens_for_user(db, existing_user.id)
        response = {
            "user": {
                "id": existing_user.id,
                "email": existing_user.email,
                "username": existing_user.username
            },
            "tokens": tokens
        }
        print("Response for existing user:", response)  # 디버깅 로그 추가
        return response
    
    # 새 사용자 생성
    new_user = UserService.create_user(db=db, user=user)
    print("Created new user:", new_user)  # 디버깅 로그 추가
    
    # 로그인 기록 저장
    login_info = LoginInfoCreate(user_id=new_user.id, action_type="login")
    LoginInfoService.create_login_info(db=db, login_info=login_info)
    
    # JWT 토큰 생성
    tokens = TokenService.create_tokens_for_user(db, new_user.id)
    response = {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username
        },
        "tokens": tokens
    }
    print("Response for new user:", response)  # 디버깅 로그 추가
    return response

@router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh 토큰을 사용하여 새로운 Access 토큰을 발급합니다.
    
    Args:
        refresh_token (str): Refresh 토큰
        db (Session): 데이터베이스 세션
    
    Returns:
        Dict: 새로운 토큰 정보
    """
    return TokenService.refresh_access_token(db, refresh_token)

@router.post("/google-logout/{user_id}", dependencies=[Depends(jwt_bearer)])
async def google_logout(user_id: int, db: Session = Depends(get_db)):
    """
    구글 로그아웃 정보를 저장합니다.
    
    Args:
        user_id (int): 로그아웃하는 사용자의 ID
        db (Session): 데이터베이스 세션
    
    Returns:
        dict: 로그아웃 성공 메시지
    """
    # 사용자 존재 확인
    user = UserService.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 로그아웃 기록 저장
    login_info = LoginInfoCreate(user_id=user_id, action_type="logout")
    LoginInfoService.create_login_info(db=db, login_info=login_info)
    
    return {"message": "로그아웃 되었습니다", "user_id": user_id}

@router.get("/login-history/{user_id}", response_model=List[LoginInfo], dependencies=[Depends(jwt_bearer)])
async def get_login_history(user_id: int, db: Session = Depends(get_db)):
    """
    사용자의 로그인/로그아웃 기록을 조회합니다.
    
    Args:
        user_id (int): 조회할 사용자의 ID
        db (Session): 데이터베이스 세션
    
    Returns:
        List[LoginInfo]: 로그인/로그아웃 기록 목록
    """
    # 사용자 존재 확인
    user = UserService.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    return LoginInfoService.get_user_login_history(db=db, user_id=user_id)
