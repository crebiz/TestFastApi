"""
FastAPI 애플리케이션의 메인 모듈
이 모듈은 FastAPI 애플리케이션의 설정과 초기화를 담당합니다.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from controller.user_controller import router as user_router
from controller.category_controller import router as category_router
from controller.hydrogen_controller import router as hydrogen_router
from database.database import engine, Base

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
    allow_origins=["http://localhost:8000"],  # 프로덕션에서는 실제 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(user_router)
app.include_router(category_router)
app.include_router(hydrogen_router)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 환경 변수 설정
if not os.getenv("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "your-secret-key-for-development-only"  # 프로덕션에서는 안전한 키로 변경

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    루트 경로 핸들러
    웹 애플리케이션의 메인 페이지를 반환합니다.
    
    Args:
        request (Request): FastAPI의 요청 객체
    
    Returns:
        HTMLResponse: index.html 템플릿을 렌더링한 응답
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID")
    })
