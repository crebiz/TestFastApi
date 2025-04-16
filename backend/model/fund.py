
from datetime import datetime
from sqlalchemy import Column, Integer, String
from backend.database.database import Base


def get_current_time():
    """
    현재 시간을 'yyyymmddhhmmss' 형식의 문자열로 반환
    
    Returns:
        str: 'yyyymmddhhmmss' 형식의 현재 시간 (예: '20250326123456')
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')

class Fund(Base):
    """
    펀드 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (int): 펀드종류 고유 식별자 (기본키)
        financial_comp (str): 금융사 이름
        type (str): 펀드 종류(개인연금/퇴직연금/투자펀드)
        account_num (str): 계좌번호
        fund_nm (str): 펀드명
        created_at (str): 계정 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 정보 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = 'fund'  # 테이블 이름

    # 컬럼정의
    id = Column(Integer, primary_key=True, index=True)  # 기본키
    financial_comp = Column(String, unique=False, index=True)  # 금융사 이름
    type = Column(String, unique=False, index=True)  # 펀드 종류
    account_num = Column(String, unique=False, index=True)  # 계좌번호
    fund_nm = Column(String, unique=False, index=True)  # 펀드명
    created_at = Column(String, default=get_current_time)  # 생성 시간
    updated_at = Column(String, default=get_current_time, onupdate=get_current_time)  # 수정 시간





