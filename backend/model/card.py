"""카드 사용내역 데이터베이스 모델 정의
이 모듈은 카드 사용내역 테이블의 구조와 기본 설정을 정의합니다.
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.database import Base
from datetime import datetime
import random

def get_current_time(as_string=True):
    """
    현재 시간을 'yyyymmddhhmmss' 형식의 문자열로 반환
    
    Args:
        as_string (bool): 문자열 반환 여부 (기본값: True)
        
    Returns:
        str 또는 datetime: 'yyyymmddhhmmss' 형식의 현재 시간 또는 datetime 객체
    """
    now = datetime.now()
    return now.strftime('%Y%m%d%H%M%S') if as_string else now

def generate_card_id():
    """
    7자리 랜덤 숫자로 구성된 카드 사용내역 ID 생성
    
    Returns:
        str: 7자리 랜덤 숫자 ID (예: '1234567')
    """
    return str(random.randint(1000000, 9999999))

class Card(Base):
    """
    카드 사용내역 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (str): 카드 사용내역 고유 식별자 (7자리 랜덤 숫자)
        transaction_date (str): 카드 이용일자 (8자리 문자열, 예: '20250430')
        card_code (str): 카드 코드 (2자리 문자열, 예: 'SH', 'LT', 'SS')
        merchant (str): 가맹점/사용처 (100자리 이내 문자열)
        amount (int): 사용 금액 (정수)
        category (str): 사용 분류 (50자리 이내 문자열, 예: '식비', '교통', '쇼핑')
        note (str): 참고사항 (100자리 이내 문자열)
        created_at (str): 데이터 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 데이터 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = "card_transactions"  # 테이블 이름

    # 컬럼 정의
    id = Column(String(7), primary_key=True, index=True, default=generate_card_id)  # 기본키, 7자리 랜덤 숫자
    transaction_date = Column(String(8), nullable=False)  # 이용일자 (YYYYMMDD)
    card_code = Column(String(2), nullable=False)  # 카드코드 (2자리)
    merchant = Column(String(100), nullable=False)  # 가맹점/사용처
    amount = Column(Integer, nullable=False)  # 사용 금액
    category = Column(String(50))  # 사용 분류 (식비, 교통, 쇼핑 등)
    note = Column(String(100))  # 참고사항
    created_at = Column(String, default=lambda: get_current_time(as_string=True))  # 생성 시간
    updated_at = Column(String, default=lambda: get_current_time(as_string=True), 
                      onupdate=lambda: get_current_time(as_string=True))  # 수정 시간
    
    def __repr__(self):
        return f"<Card(id='{self.id}', date='{self.transaction_date}', merchant='{self.merchant}', category='{self.category or ''}', amount={self.amount})>"
