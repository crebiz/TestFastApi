from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import pandas as pd
import io
import json

from backend.model.card import Card
from backend.schemas.card import CardCreate, CardUpdate
from backend.service.code_service import CodeService


class CardService:
    @staticmethod
    def get_cards(db: Session, skip: int = 0, limit: int = 100, card_code: Optional[str] = None, category: Optional[str] = None):
        """
        카드 사용내역 목록 조회
        
        Args:
            db (Session): 데이터베이스 세션
            skip (int): 건너뛸 레코드 수
            limit (int): 최대 조회 레코드 수
            card_code (str, optional): 카드 코드로 필터링
            category (str, optional): 분류로 필터링
            
        Returns:
            List[Card]: 카드 사용내역 목록
        """
        query = db.query(Card)
        
        # 카드 코드로 필터링
        if card_code:
            query = query.filter(Card.card_code == card_code)
            
        # 분류로 필터링
        if category:
            query = query.filter(Card.category == category)
            
        # 거래일자 내림차순 정렬 (최신순)
        query = query.order_by(Card.transaction_date.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_card(db: Session, card_id: str):
        """
        카드 사용내역 상세 조회
        
        Args:
            db (Session): 데이터베이스 세션
            card_id (str): 카드 사용내역 ID
            
        Returns:
            Card: 카드 사용내역 정보
        """
        return db.query(Card).filter(Card.id == card_id).first()
    
    @staticmethod
    def categorize_by_merchant(db: Session, merchant: str):
        """
        가맹점명을 기반으로 카테고리 자동 분류
        
        Args:
            db (Session): 데이터베이스 세션
            merchant (str): 가맹점명
            
        Returns:
            str: 분류된 카테고리명
        """
        # 코드 테이블에서 카드분류키워드 상세코드 조회
        category_codes = CodeService.get_code_details_by_group_id(db, "CARD_CATEGORY_KEYWORD")
        
        # 가맹점명 소문자 변환 (대소문자 구분 없이 검색)
        merchant_lower = merchant.lower()
        
        # 각 카테고리별 키워드 확인
        for code in category_codes:
            if code.description:  # description 필드에 키워드 저장
                try:
                    # description 필드에서 키워드 배열 파싱
                    keywords_data = json.loads(code.description)
                    keywords = keywords_data.get("keywords", [])
                    
                    # 키워드 매칭 확인
                    for keyword in keywords:
                        if keyword.lower() in merchant_lower:
                            return code.value  # 매칭된 카테고리 코드값 반환
                except json.JSONDecodeError:
                    # JSON 파싱 오류 무시
                    continue
        
        # 매칭되는 카테고리가 없으면 '기타' 반환
        return "기타"
    
    @staticmethod
    def create_card(db: Session, card: CardCreate):
        """
        카드 사용내역 생성
        
        Args:
            db (Session): 데이터베이스 세션
            card (CardCreate): 생성할 카드 사용내역 정보
            
        Returns:
            Card: 생성된 카드 사용내역 정보
        """
        # 카테고리가 없으면 가맹점명으로 자동 분류
        category = card.category
        if not category:
            category = CardService.categorize_by_merchant(db, card.merchant)
            
        db_card = Card(
            transaction_date=card.transaction_date,
            card_code=card.card_code,
            merchant=card.merchant,
            amount=card.amount,
            category=category,
            note=card.note
        )
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return db_card
    
    @staticmethod
    def update_card(db: Session, card_id: str, card: CardUpdate):
        """
        카드 사용내역 수정
        
        Args:
            db (Session): 데이터베이스 세션
            card_id (str): 수정할 카드 사용내역 ID
            card (CardUpdate): 수정할 내용
            
        Returns:
            Card: 수정된 카드 사용내역 정보
        """
        db_card = db.query(Card).filter(Card.id == card_id).first()
        if db_card:
            update_data = card.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_card, key, value)
            db.commit()
            db.refresh(db_card)
        return db_card
    
    @staticmethod
    def delete_card(db: Session, card_id: str):
        """
        카드 사용내역 삭제
        
        Args:
            db (Session): 데이터베이스 세션
            card_id (str): 삭제할 카드 사용내역 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        db_card = db.query(Card).filter(Card.id == card_id).first()
        if db_card:
            db.delete(db_card)
            db.commit()
            return True
        return False
    
    @staticmethod
    def process_excel_file(db: Session, file_content: bytes, card_code: str):
        """
        엑셀 파일을 처리하여 카드 사용내역 일괄 생성
        
        Args:
            db (Session): 데이터베이스 세션
            file_content (bytes): 엑셀 파일 내용
            card_code (str): 카드 코드 (예: 'SH', 'LT', 'SS')
            
        Returns:
            dict: 처리 결과 (성공 건수, 실패 건수)
        """
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(io.BytesIO(file_content))
            
            # 필요한 컬럼 확인 및 매핑
            required_columns = ['이용일자', '가맹점', '사용금액']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"필수 컬럼 '{col}'이 엑셀 파일에 없습니다.")
            
            # 데이터 처리 결과 카운터
            success_count = 0
            error_count = 0
            
            # 각 행 처리
            for _, row in df.iterrows():
                try:
                    # 날짜 형식 변환 (다양한 형식 지원)
                    date_str = str(row['이용일자']).replace('-', '').replace('.', '').replace('/', '')
                    if len(date_str) > 8:
                        date_str = date_str[:8]  # YYYYMMDD 형식으로 자르기
                    
                    # 금액 처리 (쉼표, 원 기호 등 제거)
                    amount_str = str(row['사용금액']).replace(',', '').replace('원', '').strip()
                    amount = int(float(amount_str))
                    
                    # 가맹점명 처리
                    merchant = str(row['가맹점']).strip()
                    
                    # 분류 (선택적, 없으면 자동 분류)
                    category = str(row.get('분류', '')) if '분류' in row else ''
                    if not category:
                        category = CardService.categorize_by_merchant(db, merchant)
                    
                    # 참고사항 (선택적)
                    note = str(row.get('참고사항', '')) if '참고사항' in row else ''
                    
                    # 카드 사용내역 생성
                    card_data = CardCreate(
                        transaction_date=date_str,
                        card_code=card_code,
                        merchant=merchant,
                        amount=amount,
                        category=category,
                        note=note
                    )
                    
                    CardService.create_card(db, card_data)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    continue  # 한 행의 오류가 다른 행에 영향을 주지 않도록 함
            
            return {
                "success_count": success_count,
                "error_count": error_count,
                "total_count": len(df)
            }
            
        except Exception as e:
            # 파일 처리 중 발생한 오류
            db.rollback()  # 트랜잭션 롤백
            raise ValueError(f"엑셀 파일 처리 중 오류 발생: {str(e)}")
