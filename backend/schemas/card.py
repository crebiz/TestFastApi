from typing import Optional
from pydantic import BaseModel


class CardBase(BaseModel):
    """
    카드 사용내역 기본 스키마
    
    Attributes:
        transaction_date: 카드 이용일자 (8자리 문자열, 예: '20250430')
        card_code: 카드 코드 (2자리 문자열, 예: 'SH', 'LT', 'SS')
        merchant: 가맹점/사용처 (100자리 이내 문자열)
        amount: 사용 금액 (정수)
        category: 분류 (100자리 이내 문자열, 선택적)
        note: 참고사항 (100자리 이내 문자열, 선택적)
    """
    transaction_date: str
    card_code: str
    merchant: str
    amount: int
    category: Optional[str] = None
    note: Optional[str] = None


class CardCreate(CardBase):
    """
    카드 사용내역 생성 스키마
    
    CardBase를 상속받아 생성에 필요한 필드만 포함
    """
    pass


class CardUpdate(BaseModel):
    """
    카드 사용내역 수정 스키마
    
    모든 필드가 선택적(Optional)이어서 부분 업데이트 가능
    """
    transaction_date: Optional[str] = None
    card_code: Optional[str] = None
    merchant: Optional[str] = None
    amount: Optional[int] = None
    category: Optional[str] = None
    note: Optional[str] = None


class Card(CardBase):
    """
    카드 사용내역 응답 스키마
    
    CardBase를 상속받고 추가로 id, created_at, updated_at 포함
    """
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
