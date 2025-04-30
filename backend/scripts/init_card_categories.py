"""
카드 사용내역 분류를 위한 카테고리 코드와 키워드 초기 데이터 생성 스크립트
"""
import sys
import os
import json
from sqlalchemy.orm import Session

# 상위 디렉토리를 경로에 추가하여 backend 패키지를 임포트할 수 있게 함
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.database import SessionLocal, engine
from backend.model.code import CodeGroup, CodeDetail
from backend.service.code_service import CodeService
from backend.schemas.code import CodeGroupCreate, CodeDetailCreate


def init_card_categories():
    """
    카드 분류 카테고리와 키워드 초기 데이터 생성
    """
    db = SessionLocal()
    try:
        # 이미 존재하는지 확인
        existing_group = db.query(CodeGroup).filter(CodeGroup.id == "CARD_CATEGORY_KEYWORD").first()
        if existing_group:
            print("카드 분류 카테고리 그룹코드가 이미 존재합니다.")
            return
        
        # 1. 그룹코드 생성: CARD_CATEGORY_KEYWORD
        group_data = CodeGroupCreate(
            id="CARD_CATEGORY_KEYWORD",
            name="카드 사용 분류",
            description="카드 사용내역 분류를 위한 카테고리 코드와 키워드",
            sort_order=1,
            is_active=True
        )
        
        code_group = CodeService.create_code_group(db, group_data)
        print(f"그룹코드 생성 완료: {code_group.id} - {code_group.name}")
        
        # 2. 상세코드 생성: 각 카테고리와 키워드
        categories = [
            {
                "id": "CARD_CATEGORY_KEYWORD_01",
                "name": "식비",
                "value": "식비",
                "keywords": ["식당", "레스토랑", "카페", "베이커리", "스타벅스", "커피", "맥도날드", "버거킹", "롯데리아", "피자", "치킨", "분식", "음식점"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_02",
                "name": "교통",
                "value": "교통",
                "keywords": ["택시", "버스", "지하철", "기차", "KTX", "SRT", "주유소", "주차장", "톨게이트", "고속도로", "하이패스"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_03",
                "name": "쇼핑",
                "value": "쇼핑",
                "keywords": ["마트", "백화점", "이마트", "홈플러스", "롯데마트", "코스트코", "쿠팡", "11번가", "지마켓", "옥션", "편의점", "GS25", "CU", "세븐일레븐"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_04",
                "name": "의료",
                "value": "의료",
                "keywords": ["병원", "약국", "의원", "치과", "안과", "피부과", "한의원", "건강검진", "의료원"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_05",
                "name": "문화",
                "value": "문화",
                "keywords": ["영화관", "CGV", "메가박스", "롯데시네마", "공연", "콘서트", "전시회", "박물관", "미술관", "도서관", "서점", "교보문고"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_06",
                "name": "여행",
                "value": "여행",
                "keywords": ["호텔", "리조트", "펜션", "에어비앤비", "항공", "대한항공", "아시아나", "여행사", "투어", "렌터카"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_07",
                "name": "통신",
                "value": "통신",
                "keywords": ["통신요금", "SKT", "KT", "LG", "휴대폰", "인터넷", "유선전화", "통신사"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_08",
                "name": "교육",
                "value": "교육",
                "keywords": ["학원", "교육원", "강의", "수강료", "학비", "교재", "교육비", "학습지", "대학", "등록금"]
            },
            {
                "id": "CARD_CATEGORY_KEYWORD_09",
                "name": "기타",
                "value": "기타",
                "keywords": []
            }
        ]
        
        for category in categories:
            # description 필드에 키워드 배열을 JSON 형태로 저장
            keywords_json = json.dumps({"keywords": category["keywords"]}, ensure_ascii=False)
            
            detail_data = CodeDetailCreate(
                id=category["id"],
                group_id="CARD_CATEGORY_KEYWORD",
                name=category["name"],
                value=category["value"],
                description=keywords_json,
                sort_order=int(category["id"].split("_")[-1]),
                is_active=True
            )
            
            code_detail = CodeService.create_code_detail(db, detail_data)
            print(f"상세코드 생성 완료: {code_detail.id} - {code_detail.name} (키워드 {len(category['keywords'])}개)")
        
        print("카드 분류 카테고리 초기 데이터 생성 완료")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_card_categories()
    print("스크립트 실행 완료")
