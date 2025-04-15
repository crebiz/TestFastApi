"""
JWT(JSON Web Token) 인증을 처리하는 미들웨어 모듈.
이 모듈은 FastAPI 애플리케이션에서 보호된 엔드포인트에 대한 접근을 제어합니다.
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from service.token_service import TokenService


class JWTBearer(HTTPBearer):
    """
    JWT 베어러 토큰 인증을 처리하는 커스텀 클래스.
    FastAPI의 HTTPBearer를 상속받아 JWT 특화 기능을 추가합니다.
    """
    
    def __init__(self, auto_error: bool = True):
        """
        JWTBearer 클래스 초기화
        
        Args:
            auto_error (bool): True일 경우 인증 실패 시 자동으로 에러를 발생시킴
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        각 요청에 대한 JWT 토큰 검증을 수행하는 메서드
        
        Args:
            request (Request): FastAPI의 요청 객체
            
        Returns:
            str: 유효한 JWT 토큰 문자열
            
        Raises:
            HTTPException: 인증 실패 시 403 Forbidden 에러 발생
        """
        # 상위 클래스의 __call__ 메서드를 호출하여 인증 정보 추출
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        
        # 인증 정보가 없는 경우 에러 발생
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code"
            )
        
        # Bearer 토큰 방식이 아닌 경우 에러 발생    
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme"
            )
        
        try:
            # JWT 토큰 검증 및 페이로드 추출
            payload = TokenService.verify_token(credentials.credentials)
            # 요청 상태에 사용자 ID 저장 (후속 처리에서 사용 가능)
            request.state.user_id = int(payload.get("sub"))
        except Exception as e:
            # 토큰 검증 실패 시 에러 발생
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
            
        return credentials.credentials

# 전역 JWT 베어러 인스턴스 생성
jwt_bearer = JWTBearer()
