from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd
import io
import json
import logging
import os
import logging.handlers
import re

# 로깅 설정
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('card_service')
logger.setLevel(logging.INFO)

# 파일 핸들러 설정 - card_controller.log 파일에 로그 추가
log_file = os.path.join(log_dir, 'card_controller.log')
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
)
file_handler.setLevel(logging.INFO)

# 포맷 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 콘솔 핸들러 추가
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 핸들러 추가
logger.addHandler(file_handler)
logger.addHandler(console_handler)

from backend.model.card import Card
from backend.schemas.card import CardCreate, CardUpdate
from backend.schemas.card_statistics import CardStatistics, MerchantStat, CategoryStat, CardCompanyStat, MonthlyStat
from backend.service.code_service import CodeService
from collections import defaultdict
from datetime import datetime, timedelta


class CardService:
    @staticmethod
    def get_all_monthly_stats(db: Session):
        """
        전체 데이터의 월별 통계 조회 (선택한 월과 상관없이 전체 데이터 기반)
        
        Args:
            db (Session): 데이터베이스 세션
            
        Returns:
            List[MonthlyStat]: 월별 통계 데이터 리스트
        """
        # 현재 날짜 기준으로 최근 12개월 기간 생성
        current_date = datetime.now()
        months = []
        
        # 현재 월부터 11개월 전까지 추가 (총 12개월)
        for i in range(11, -1, -1):
            # i개월 전 날짜 계산
            past_date = current_date - timedelta(days=i*30)  # 대략적인 월 계산
            month_key = f"{past_date.year}-{past_date.month:02d}"
            months.append(month_key)
        
        # 기본 데이터 초기화 (12개월 전부 0으로 초기화)
        monthly_stats = {month: {'amount': 0, 'count': 0} for month in months}
        
        # 모든 카드 사용내역 조회 (필터링 없이 전체 데이터)
        cards = db.query(Card).all()
        
        # 실제 데이터로 채우기
        for card in cards:
            # 거래일자에서 연월 추출 (YYYYMMDD -> YYYY-MM)
            if len(card.transaction_date) >= 6:
                year = card.transaction_date[:4]
                month = card.transaction_date[4:6]
                month_key = f"{year}-{month}"
                
                # 최근 12개월 데이터에 포함된 월인 경우에만 추가
                if month_key in monthly_stats:
                    monthly_stats[month_key]['amount'] += card.amount
                    monthly_stats[month_key]['count'] += 1
        
        # 연월 정렬을 위해 리스트로 변환
        monthly_stats_items = [(month, stats) for month, stats in monthly_stats.items()]
        # 연월 순으로 정렬
        monthly_stats_items.sort(key=lambda x: x[0])
        
        # MonthlyStat 객체 리스트로 변환
        return [
            MonthlyStat(month=month, amount=stats['amount'], count=stats['count'])
            for month, stats in monthly_stats_items
        ]
    
    @staticmethod
    def get_card_statistics(db: Session, card_code: Optional[str] = None, year: Optional[int] = None, month: Optional[int] = None):
        """
        카드 사용내역 통계 조회
        
        Args:
            db (Session): 데이터베이스 세션
            card_code (str, optional): 카드 코드로 필터링
            year (int, optional): 연도로 필터링
            month (int, optional): 월로 필터링
            
        Returns:
            CardStatistics: 카드 사용내역 통계
        """
        # 필터링된 쿼리 생성
        query = db.query(Card)
        
        # 카드 코드로 필터링
        if card_code:
            query = query.filter(Card.card_code == card_code)
            
        # 연도로 필터링
        if year:
            year_str = str(year)
            query = query.filter(Card.transaction_date.like(f'{year_str}%'))
            
        # 월로 필터링
        if month:
            month_str = str(month).zfill(2)  # 1자리 월은 앞에 0 붙임 (1 -> 01)
            
            if year:
                # 연도와 월이 모두 있는 경우 (YYYYMM 형식으로 필터링)
                year_str = str(year)
                query = query.filter(Card.transaction_date.like(f'{year_str}{month_str}%'))
            else:
                # 월만 있는 경우 (연도 관계없이 해당 월만 필터링)
                query = query.filter(Card.transaction_date.like(f'_____{month_str}%'))
        
        # 모든 카드 사용내역 조회 (페이지네이션 없이 전체 데이터)
        cards = query.all()
        
        # 총 사용금액 및 건수
        total_amount = sum(card.amount for card in cards)
        total_count = len(cards)
        
        # 가맹점별 통계 계산
        merchant_stats = defaultdict(lambda: {'amount': 0, 'count': 0})
        for card in cards:
            merchant_stats[card.merchant]['amount'] += card.amount
            merchant_stats[card.merchant]['count'] += 1
        
        # 최대 지출 가맹점 찾기
        top_amount_merchant = {'name': '-', 'amount': 0, 'count': 0}
        for merchant, stats in merchant_stats.items():
            if stats['amount'] > top_amount_merchant['amount']:
                top_amount_merchant = {
                    'name': merchant,
                    'amount': stats['amount'],
                    'count': stats['count']
                }
        
        # 최다 방문 가맹점 찾기
        top_visit_merchant = {'name': '-', 'amount': 0, 'count': 0}
        for merchant, stats in merchant_stats.items():
            if stats['count'] > top_visit_merchant['count']:
                top_visit_merchant = {
                    'name': merchant,
                    'amount': stats['amount'],
                    'count': stats['count']
                }
        
        # 카테고리별 통계 계산
        category_stats = defaultdict(lambda: {'amount': 0, 'count': 0})
        for card in cards:
            category = card.category or '기타'
            category_stats[category]['amount'] += card.amount
            category_stats[category]['count'] += 1
        
        # 카드사별 통계 계산
        card_company_stats = defaultdict(lambda: {'amount': 0, 'count': 0})
        for card in cards:
            card_company_stats[card.card_code]['amount'] += card.amount
            card_company_stats[card.card_code]['count'] += 1
            
        # 월별 통계 계산 - 최근 12개월 데이터 생성
        from datetime import datetime, timedelta
        
        # 현재 날짜 기준으로 최근 12개월 기간 생성
        current_date = datetime.now()
        months = []
        
        # 현재 월부터 11개월 전까지 추가 (총 12개월)
        for i in range(11, -1, -1):
            # i개월 전 날짜 계산
            past_date = current_date - timedelta(days=i*30)  # 대략적인 월 계산
            month_key = f"{past_date.year}-{past_date.month:02d}"
            months.append(month_key)
        
        # 기본 데이터 초기화 (12개월 전부 0으로 초기화)
        monthly_stats = {month: {'amount': 0, 'count': 0} for month in months}
        
        # 실제 데이터로 채우기
        for card in cards:
            # 거래일자에서 연월 추출 (YYYYMMDD -> YYYY-MM)
            if len(card.transaction_date) >= 6:
                year = card.transaction_date[:4]
                month = card.transaction_date[4:6]
                month_key = f"{year}-{month}"
                
                # 최근 12개월 데이터에 포함된 월인 경우에만 추가
                if month_key in monthly_stats:
                    monthly_stats[month_key]['amount'] += card.amount
                    monthly_stats[month_key]['count'] += 1
        
        # 연월 정렬을 위해 리스트로 변환
        monthly_stats_items = [(month, stats) for month, stats in monthly_stats.items()]
        # 연월 순으로 정렬
        monthly_stats_items.sort(key=lambda x: x[0])
        
        # 결과 변환
        category_stats_list = [
            CategoryStat(name=category, amount=stats['amount'], count=stats['count'])
            for category, stats in category_stats.items()
        ]
        
        card_company_stats_list = [
            CardCompanyStat(name=card_code, amount=stats['amount'], count=stats['count'])
            for card_code, stats in card_company_stats.items()
        ]
        
        monthly_stats_list = [
            MonthlyStat(month=month, amount=stats['amount'], count=stats['count'])
            for month, stats in monthly_stats_items
        ]
        
        # 통계 결과 반환
        return CardStatistics(
            total_amount=total_amount,
            total_count=total_count,
            top_amount_merchant=MerchantStat(
                name=top_amount_merchant['name'],
                amount=top_amount_merchant['amount'],
                count=top_amount_merchant['count']
            ),
            top_visit_merchant=MerchantStat(
                name=top_visit_merchant['name'],
                amount=top_visit_merchant['amount'],
                count=top_visit_merchant['count']
            ),
            category_stats=category_stats_list,
            card_company_stats=card_company_stats_list,
            monthly_stats=monthly_stats_list
        )
        
    @staticmethod
    def get_cards(db: Session, skip: int = 0, limit: int = 100, card_code: Optional[str] = None, category: Optional[str] = None, year: Optional[int] = None, month: Optional[int] = None):
        """
        카드 사용내역 목록 조회
        
        Args:
            db (Session): 데이터베이스 세션
            skip (int): 건너뛸 레코드 수
            limit (int): 최대 조회 레코드 수
            card_code (str, optional): 카드 코드로 필터링
            category (str, optional): 분류로 필터링
            year (int, optional): 연도로 필터링
            month (int, optional): 월로 필터링
            
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
        
        # 연도로 필터링
        if year:
            # transaction_date 필드에서 연도 추출하여 필터링 (YYYYMMDD 형식의 앞 4자리)
            year_str = str(year)
            query = query.filter(Card.transaction_date.like(f'{year_str}%'))
            
        # 월로 필터링
        if month:
            # transaction_date 필드에서 월 추출하여 필터링 (YYYYMMDD 형식의 5-6번째 자리)
            # 1자리 월은 앞에 0 붙임 (1월 -> 01)
            month_str = str(month).zfill(2)  # 1자리 월은 앞에 0 붙임 (1 -> 01)
            
            if year:
                # 연도와 월이 모두 있는 경우 (YYYYMM 형식으로 필터링)
                year_str = str(year)
                query = query.filter(Card.transaction_date.like(f'{year_str}{month_str}%'))
            else:
                # 월만 있는 경우 (연도 관계없이 해당 월만 필터링)
                query = query.filter(Card.transaction_date.like(f'_____{month_str}%'))
                # _는 아무 문자나 매칭하는 SQL LIKE 패턴
            
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
    def extract_card_code_from_excel(df: pd.DataFrame) -> str:
        """
        엑셀 파일의 내용을 분석하여 카드코드 추출
        
        Args:
            df (pd.DataFrame): 엑셀 파일 데이터프레임
            
        Returns:
            str: 추출된 카드코드 ('SH', 'LT', 'SS', 'HD', 'HN', 'KB' 등)
        """
        # 카드사 정보와 코드 매핑
        card_company_mapping = {
            '신한': 'SH',
            '신한카드': 'SH',
            '롯데': 'LT',
            '롯데카드': 'LT',
            '삼성': 'SS',
            '삼성카드': 'SS',
            '현대': 'HD',
            '현대카드': 'HD',
            '하나': 'HN',
            '하나카드': 'HN',
            '국민': 'KB',
            '국민카드': 'KB',
            'shinhan': 'SH',
            'lotte': 'LT',
            'samsung': 'SS',
            'hyundai': 'HD',
            'hana': 'HN',
            'kookmin': 'KB',
            'kb': 'KB'
        }
        
        # 1. 컴럼명 확인
        for col in df.columns:
            col_lower = str(col).lower()
            # 컴럼명에 카드사 정보가 있는지 확인
            for card_name, code in card_company_mapping.items():
                if card_name.lower() in col_lower:
                    logger.info(f"컴럼명 '{col}'에서 카드사 '{card_name}' 발견, 코드: {code}")
                    return code
        
        # 2. 첫 번째 행 확인 (제목이나 메타데이터에 카드사 정보가 있을 수 있음)
        if len(df) > 0:
            first_row = df.iloc[0]
            for value in first_row.astype(str):
                value_lower = value.lower()
                for card_name, code in card_company_mapping.items():
                    if card_name.lower() in value_lower:
                        logger.info(f"첫 번째 행에서 카드사 '{card_name}' 발견, 코드: {code}")
                        return code
        
        # 3. 전체 데이터 조회 (일부 데이터만 샘플링)
        sample_size = min(10, len(df))  # 최대 10행까지만 확인
        for _, row in df.head(sample_size).iterrows():
            for value in row.astype(str):
                value_lower = value.lower()
                for card_name, code in card_company_mapping.items():
                    if card_name.lower() in value_lower:
                        logger.info(f"데이터에서 카드사 '{card_name}' 발견, 코드: {code}")
                        return code
        
        # 기본값: 신한카드
        logger.warning("엑셀 파일에서 카드사 정보를 추출할 수 없어 기본값 'SH'(신한카드) 사용")
        return 'SH'
    
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
        category_codes = CodeService.get_code_details(db, group_id="CARD_CATEGORY_KEYWORD")
        
        # 가맹점명 소문자 변환 (대소문자 구분 없이 검색)
        merchant_lower = merchant.lower()
        
        # 각 카테고리별 키워드 확인
        for code in category_codes:
            if code.description:  # description 필드에 키워드 저장
                try:
                    # description 필드에서 키워드 배열 파싱
                    logger.info(f"Description 필드 내용: {code.description}, 타입: {type(code.description)}")
                    
                    dictDescription = CardService.parse_keywords_string(code.description)
                    logger.info(f"dictDescription 필드 내용: {dictDescription}")

                    # 데이터 형식에 따라 처리
                    if isinstance(dictDescription, dict):
                        # 이미 디셔너리인 경우
                        keywords = dictDescription.get("keywords", [])
                        logger.info(f"keywords 필드 내용: {keywords}")
                    else:
                        try:
                            # 문자열인 경우 JSON 파싱 시도
                            keywords_data = json.loads(code.description)
                            logger.info(f"keywords_data 필드 내용: {keywords_data}")
                            if isinstance(keywords_data, dict):
                                keywords = keywords_data.get("keywords", [])
                                logger.info(f"keywords_data keywords 필드 내용: {keywords}")
                            else:
                                # 배열이나 다른 형태인 경우
                                keywords = keywords_data if isinstance(keywords_data, list) else []
                        except json.JSONDecodeError:
                            # JSON 파싱 실패 시 문자열 형식 키워드 파싱 시도
                            logger.info(f"JSON 파싱 실패, 문자열 형식 키워드 파싱 시도: {code.description}")
                            keywords = CardService.parse_keywords_string(code.description)
                            logger.info(f"문자열에서 파싱된 키워드: {keywords}")
                    
                    logger.info(f"추출된 키워드: {keywords}")
                    
                    # 키워드 매칭 확인
                    for keyword in keywords:
                        if keyword and keyword.lower() in merchant_lower:
                            logger.info(f"키워드 매칭 성공: {keyword} in {merchant}")
                            return code.name  # 매칭된 카테고리의 name 값 반환
                except Exception as e:
                    # 모든 예외 처리 및 로깅
                    logger.error(f"키워드 파싱 중 오류 발생: {str(e)}")
                    continue
        
        # 매칭되는 카테고리가 없으면 '기타' 반환
        return "기타"
    
    @staticmethod
    def parse_keywords_string(keywords_str: str) -> dict:
        """
        문자열 형식의 키워드를 리스트로 파싱
        예: "키워드1", "키워드2", "키워드3" -> ["키워드1", "키워드2", "키워드3"]
        
        Args:
            keywords_str (str): 키워드 문자열
            
        Returns:
            dict: 키워드 리스트를 포함한 딕셔너리 {"keywords": [...]} 형식
        """
        if not keywords_str or keywords_str.strip() == "":
            return {"keywords": []}
        
        # 쌍따옴표로 둘러싸인 문자열 추출
        pattern = r'"([^"]*)"'
        keywords = re.findall(pattern, keywords_str)
        
        # 쉼표로 구분된 문자열 처리 (쌍따옴표가 없는 경우)
        if not keywords:
            keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
        
        return {"keywords": keywords}
    
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
    def process_excel_file(db: Session, file_content: bytes, use_month: str):
        """
        엑셀 파일을 처리하여 카드 사용내역 일괄 생성
        엑셀 파일에서 카드코드를 추출하거나, 지정된 카드코드 사용
        엑셀 파일 업로드 시 동일한 card_code를 가진 기존 데이터를 모두 삭제함
        
        Args:
            db (Session): 데이터베이스 세션
            file_content (bytes): 엑셀 파일 내용
            card_code (Optional[str]): 카드 코드 (예: 'SH', 'LT', 'SS'). None이면 엑셀에서 추출
            
        Returns:
            dict: 처리 결과 (성공 건수, 실패 건수)
        """
        try:
            # 엑셀 파일 읽기
            logger.info(f"엑셀 파일 읽기 시작: 파일 크기 {len(file_content)} 바이트")
            df = pd.read_excel(io.BytesIO(file_content))
            logger.info(f"엑셀 파일 읽기 성공: {len(df)} 행 발견")
            logger.info(f"엑셀 파일 컴럼: {df.columns.tolist()}")
                        
            # 동일한 useMonth 가진 기존 데이터 삭제
            logger.info(f"use_month={use_month}인 기존 데이터 삭제 시작")
            deleted_count = db.query(Card).filter(Card.transaction_date.like(f'%{use_month}%')).delete()
            logger.info(f"use_month={use_month}인 기존 데이터 {deleted_count}건 삭제 완료")
            db.commit()
            
            # 필요한 컴럼 확인 및 매핑
            required_columns = ['이용일자', '카드코드', '가맹점', '사용금액']
            for col in required_columns:
                if col not in df.columns:
                    logger.error(f"필수 컴럼 '{col}'이 엑셀 파일에 없습니다. 발견된 컴럼: {df.columns.tolist()}")
                    raise ValueError(f"필수 컴럼 '{col}'이 엑셀 파일에 없습니다.")
            
            # 데이터 처리 결과 카운터
            success_count = 0
            error_count = 0
            
            # 각 행 처리
            for _, row in df.iterrows():
                try:
                    # 로그를 통해 현재 처리중인 행 데이터 확인
                    logger.info(f"행 처리 시작: {dict(row)}")
                    
                    # 날짜 형식 변환 (다양한 형식 지원)
                    date_str = str(row['이용일자']).replace('-', '').replace('.', '').replace('/', '')
                    if len(date_str) > 8:
                        date_str = date_str[:8]  # YYYYMMDD 형식으로 자르기
                    logger.info(f"날짜 처리 결과: {date_str}")
                    
                    # 금액 처리 (콤마, 원 기호 등 제거)
                    amount_str = str(row['사용금액']).replace(',', '').replace('원', '').strip()
                    amount = int(float(amount_str))
                    logger.info(f"금액 처리 결과: {amount}")
                    
                    # 카드코드 처리
                    card_code = str(row['카드코드']).strip()
                    logger.info(f"카드코드 처리 결과: {card_code}")
                    
                    # 가맹점명 처리
                    merchant = str(row['가맹점']).strip()
                    logger.info(f"가맹점 처리 결과: {merchant}")
                    
                    # 분류 (선택적, 없으면 자동 분류)
                    category = str(row['가맹점']).strip()
                    if category:
                        logger.info(f"카테고리 자동 분류 시작: 가맹점={merchant}")
                        category = CardService.categorize_by_merchant(db, merchant)
                        logger.info(f"카테고리 자동 분류 결과: {category}")
                    
                    # 참고사항 (선택적)
                    # note = str(row.get('참고사항', '')) if '참고사항' in row else ''
                    
                    # 카드 사용내역 생성
                    card_data = CardCreate(
                        transaction_date=date_str,
                        card_code=card_code,
                        merchant=merchant,
                        amount=amount,
                        category=category
                    )
                    logger.info(f"카드 사용내역 생성: {card_data}")
                    CardService.create_card(db, card_data)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"행 처리 오류: {str(e)}")
                    continue  # 한 행의 오류가 다른 행에 영향을 주지 않도록 함
            
            return {
                "deleted_count": deleted_count,
                "success_count": success_count,
                "error_count": error_count,
                "total_count": len(df)
            }
            
        except Exception as e:
            # 파일 처리 중 발생한 오류
            logger.error(f"엑셀 파일 처리 중 오류 발생: {str(e)}")
            db.rollback()  # 트랜잭션 롤백
            raise ValueError(f"엑셀 파일 처리 중 오류 발생: {str(e)}")
