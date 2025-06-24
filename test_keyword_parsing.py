"""
키워드 파싱 및 카테고리 분류 테스트 스크립트
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys

# 프로젝트 루트 디렉토리를 파이썬 경로에 추가
sys.path.append('.')

from backend.service.card_service import CardService

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 URL 설정
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234qwer")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def test_keyword_parsing():
    """문자열 형식 키워드 파싱 테스트"""
    print("=== 키워드 파싱 테스트 ===")
    
    # 테스트 케이스 1: 쌍따옴표와 쉼표로 구분된 문자열
    test_str1 = '"식당", "레스토랑", "카페", "베이커리"'
    keywords1 = CardService.parse_keywords_string(test_str1)
    print(f"원본 문자열: {test_str1}")
    print(f"파싱된 키워드: {keywords1}")
    
    # 테스트 케이스 2: 쉼표로만 구분된 문자열
    test_str2 = "식당,레스토랑,카페,베이커리"
    keywords2 = CardService.parse_keywords_string(test_str2)
    print(f"원본 문자열: {test_str2}")
    print(f"파싱된 키워드: {keywords2}")
    
    # 테스트 케이스 3: 빈 문자열
    test_str3 = ""
    keywords3 = CardService.parse_keywords_string(test_str3)
    print(f"원본 문자열: {test_str3}")
    print(f"파싱된 키워드: {keywords3}")

def test_merchant_categorization():
    """가맹점 카테고리 분류 테스트"""
    print("\n=== 가맹점 분류 테스트 ===")
    
    # 데이터베이스 연결
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 테스트 케이스 1: 식비 카테고리 (스타벅스)
        merchant1 = "스타벅스 강남점"
        category1 = CardService.categorize_by_merchant(db, merchant1)
        print(f"가맹점: {merchant1} -> 카테고리: {category1}")
        
        # 테스트 케이스 2: 교통비 카테고리 (택시)
        merchant2 = "카카오택시"
        category2 = CardService.categorize_by_merchant(db, merchant2)
        print(f"가맹점: {merchant2} -> 카테고리: {category2}")
        
        # 테스트 케이스 3: 매칭되지 않는 가맹점
        merchant3 = "알 수 없는 가맹점"
        category3 = CardService.categorize_by_merchant(db, merchant3)
        print(f"가맹점: {merchant3} -> 카테고리: {category3}")
    finally:
        db.close()

if __name__ == "__main__":
    test_keyword_parsing()
    test_merchant_categorization()
