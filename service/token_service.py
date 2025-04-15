"""
JWT(JSON Web Token) 토큰 관리를 위한 서비스 모듈

이 모듈은 다음과 같은 기능을 제공합니다:
1. Access Token 생성 및 검증
2. Refresh Token 생성 및 검증
3. 토큰 만료 시간 관리
4. 토큰 데이터베이스 저장 및 관리
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import jwt
from model.token import Token
from schemas.token import TokenCreate
import os
import secrets

# 환경 변수에서 설정 가져오기 또는 안전한 기본값 설정
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))  # JWT 서명에 사용할 비밀키
ALGORITHM = "HS256"  # JWT 암호화 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Access 토큰 만료 시간 (분)
REFRESH_TOKEN_EXPIRE_DAYS = 7    # Refresh 토큰 만료 시간 (일)

class TokenService:
    """
    JWT 토큰 관리를 위한 서비스 클래스
    Access Token과 Refresh Token의 생성, 검증, 갱신을 처리합니다.
    """

    @staticmethod
    def create_access_token(data: dict) -> Tuple[str, datetime]:
        """
        Access Token을 생성합니다.
        
        Args:
            data (dict): 토큰에 포함될 데이터 (주로 사용자 ID 등)
            
        Returns:
            Tuple[str, datetime]: (생성된 JWT 토큰, 만료 시간)
            
        Note:
            - 만료 시간은 현재 시간 + ACCESS_TOKEN_EXPIRE_MINUTES
            - 토큰 타입은 'access'로 지정됨
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt, expire

    @staticmethod
    def create_refresh_token(data: dict) -> Tuple[str, datetime]:
        """
        Refresh Token을 생성합니다.
        
        Args:
            data (dict): 토큰에 포함될 데이터 (주로 사용자 ID 등)
            
        Returns:
            Tuple[str, datetime]: (생성된 JWT 토큰, 만료 시간)
            
        Note:
            - 만료 시간은 현재 시간 + REFRESH_TOKEN_EXPIRE_DAYS
            - 토큰 타입은 'refresh'로 지정됨
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt, expire

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> dict:
        """
        JWT 토큰을 검증하고 페이로드를 반환합니다.
        
        Args:
            token (str): 검증할 JWT 토큰
            token_type (str): 예상되는 토큰 타입 ('access' 또는 'refresh')
            
        Returns:
            dict: 토큰의 페이로드 데이터
            
        Raises:
            HTTPException: 토큰이 유효하지 않거나, 만료되었거나, 타입이 일치하지 않을 경우
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # 토큰 타입 검증
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type} token.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def create_tokens_for_user(db: Session, user_id: int) -> Dict:
        """
        사용자를 위한 Access Token과 Refresh Token을 생성합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            user_id (int): 토큰을 생성할 사용자의 ID
            
        Returns:
            Dict:
                'access_token': str,
                'refresh_token': str,
                'token_type': 'bearer'
            
        Note:
            - Refresh 토큰은 데이터베이스에 저장됨
            - 이전 Refresh 토큰이 있다면 새로운 토큰으로 교체됨
        """
        access_token, access_token_expires = TokenService.create_access_token(
            data={"sub": str(user_id)}
        )
        refresh_token, refresh_token_expires = TokenService.create_refresh_token(
            data={"sub": str(user_id)}
        )

        # 기존 토큰이 있다면 삭제
        db.query(Token).filter(Token.user_id == user_id).delete()
        
        # 새 토큰 생성
        token_data = TokenCreate(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires=access_token_expires,
            refresh_token_expires=refresh_token_expires
        )
        
        db_token = Token(
            user_id=token_data.user_id,
            access_token=token_data.access_token,
            refresh_token=token_data.refresh_token,
            access_token_expires=token_data.access_token_expires,
            refresh_token_expires=token_data.refresh_token_expires
        )
        
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Dict:
        """
        Refresh Token을 사용하여 새로운 Access Token을 발급합니다.
        
        Args:
            db (Session): 데이터베이스 세션
            refresh_token (str): 유효한 Refresh Token
            
        Returns:
            Dict:
                'access_token': str,
                'token_type': 'bearer'
            
        Raises:
            HTTPException: Refresh Token이 유효하지 않거나 데이터베이스에서 찾을 수 없는 경우
        """
        # Refresh Token 검증
        payload = TokenService.verify_token(refresh_token, token_type="refresh")
        user_id = int(payload["sub"])
        
        # DB에서 토큰 확인
        db_token = db.query(Token).filter(Token.user_id == user_id).first()
        if not db_token or db_token.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 새로운 액세스 토큰 생성
        new_access_token, new_access_expires = TokenService.create_access_token(
            data={"sub": str(user_id)}
        )
        
        # DB 업데이트
        db_token.access_token = new_access_token
        db_token.access_token_expires = new_access_expires
        db.commit()
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
