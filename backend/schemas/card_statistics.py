from typing import Dict, List, Optional
from pydantic import BaseModel


class MerchantStat(BaseModel):
    """
    가맹점 통계 스키마
    
    Attributes:
        name: 가맹점명
        amount: 총 사용금액
        count: 방문 횟수
    """
    name: str
    amount: int
    count: int


class CategoryStat(BaseModel):
    """
    카테고리 통계 스키마
    
    Attributes:
        name: 카테고리명
        amount: 총 사용금액
        count: 건수
    """
    name: str
    amount: int
    count: int


class CardCompanyStat(BaseModel):
    """
    카드사 통계 스키마
    
    Attributes:
        name: 카드사명
        amount: 총 사용금액
        count: 건수
    """
    name: str
    amount: int
    count: int


class MonthlyStat(BaseModel):
    """
    월별 통계 스키마
    
    Attributes:
        month: 연월(예: '2025-01')
        amount: 총 사용금액
        count: 건수
    """
    month: str
    amount: int
    count: int


class CardStatistics(BaseModel):
    """
    카드 사용내역 통계 스키마
    
    Attributes:
        total_amount: 총 사용금액
        total_count: 총 건수
        top_amount_merchant: 최대 지출 가맹점
        top_visit_merchant: 최다 방문 가맹점
        category_stats: 카테고리별 통계
        card_company_stats: 카드사별 통계
        monthly_stats: 월별 통계 데이터
    """
    total_amount: int
    total_count: int
    top_amount_merchant: MerchantStat
    top_visit_merchant: MerchantStat
    category_stats: List[CategoryStat]
    card_company_stats: List[CardCompanyStat]
    monthly_stats: List[MonthlyStat]
