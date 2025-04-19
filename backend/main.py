"""
FastAPI 애플리케이션의 메인 모듈
이 모듈은 FastAPI 애플리케이션의 설정과 초기화를 담당합니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend.controller.user_controller import router as user_router
from backend.controller.category_controller import router as category_router
from backend.controller.hydrogen_controller import router as hydrogen_router
from backend.controller.fund_controller import router as fund_router
from backend.controller.kftc_controller import router as kftc_router
from backend.database.database import engine, Base

# 환경 변수 로드
load_dotenv()

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="TestFastApi Backend",
    description="사용자 관리를 위한 RESTful API",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router)
app.include_router(category_router)
app.include_router(hydrogen_router)
app.include_router(fund_router)
app.include_router(kftc_router)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 환경 변수 설정
if not os.getenv("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "your-secret-key-for-development-only"  # 프로덕션에서는 안전한 키로 변경

@app.get("/")
async def root():
    """
    루트 경로 핸들러
    API가 작동 중임을 확인하는 메시지를 반환합니다.
    
    Returns:
        dict: 환영 메시지와 API 상태
    """
    return {
        "message": "TestFastApi Backend API",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/api/config")
async def get_config():
    """
    프론트엔드에 필요한 설정 정보를 제공합니다.
    
    Returns:
        dict: 설정 정보
    """
    return {
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID")
    }
