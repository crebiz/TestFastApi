"""
데이터베이스 연결 및 세션 관리
이 모듈은 PostgreSQL 데이터베이스 연결 설정과 세션 관리를 담당합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# 데이터베이스 연결 URL 설정
# 환경 변수에서 개별 데이터베이스 설정을 가져와서 URL 생성
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1qaz2wsx")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 팩토리 생성
# autocommit=False: 명시적 커밋 필요
# autoflush=False: 명시적 플러시 필요
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델의 기본 클래스
Base = declarative_base()

# 데이터베이스 초기화 함수
def init_db():
    """데이터베이스 초기화 함수"""
    # 기존 테이블 모두 삭제
    Base.metadata.drop_all(bind=engine)
    # 새로운 테이블 생성
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    데이터베이스 세션 생성 및 관리를 위한 제너레이터 함수
    
    Yields:
        Session: 데이터베이스 세션 객체
    
    Note:
        FastAPI의 의존성 주입 시스템에서 사용됩니다.
        세션은 요청 처리가 완료되면 자동으로 닫힙니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
