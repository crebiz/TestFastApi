
from datetime import datetime
from sqlalchemy import Column, String, event, select, func
from sqlalchemy.ext.declarative import declared_attr
from backend.database.database import Base, engine
from backend.utils.common import get_current_time

class Fund(Base):
    """
    펀드 정보를 저장하는 데이터베이스 모델
    
    Attributes:
        id (str): 펀드종류 고유 식별자 (기본키, 'F001', 'F002' 형식)
        financial_comp (str): 금융사 이름
        type (str): 펀드 종류(개인연금/퇴직연금/투자펀드)
        account_num (str): 계좌번호
        fund_nm (str): 펀드명
        state (str): 펀드상태태
        created_at (str): 계정 생성 시간 ('yyyymmddhhmmss' 형식)
        updated_at (str): 정보 수정 시간 ('yyyymmddhhmmss' 형식)
    """
    __tablename__ = 'fund'  # 테이블 이름

    # 컬럼정의
    id = Column(String(10), primary_key=True, index=True)  # 기본키 (F001, F002 형식)
    financial_comp = Column(String, unique=False, index=True)  # 금융사 이름
    type = Column(String, unique=False, index=True)  # 펀드 종류
    account_num = Column(String, unique=False, index=True)  # 계좌번호
    fund_nm = Column(String, unique=False, index=True)  # 펀드명
    state = Column(String, unique=False, index=True)  # 펀드상태
    invest_type = Column(String, nullable=True, index=True)  # 투자유형
    note = Column(String, nullable=True, index=True)  # 참고사항
    created_at = Column(String, default=lambda: get_current_time(as_string=True))  # 생성 시간
    updated_at = Column(String, default=lambda: get_current_time(as_string=True), onupdate=lambda: get_current_time(as_string=True))  # 수정 시간


# 펀드 ID 자동 생성 함수
def generate_fund_id(context):
    """F001, F002 형식의 펀드 ID를 자동 생성"""
    # 현재 세션 가져오기
    connection = context['get_bind']()
    
    # 마지막 펀드 ID 조회
    result = connection.execute(select(Fund.id).order_by(Fund.id.desc()).limit(1)).scalar()
    
    if result:
        # 기존 ID에서 숫자 부분 추출 후 증가
        num = int(result[1:]) + 1
    else:
        # 첫 번째 펀드인 경우
        num = 1
    
    # 새 ID 생성 (F001, F002 형식)
    new_id = f"F{num:03d}"
    return new_id

# 펀드 생성 전 이벤트 리스너 등록
@event.listens_for(Fund, 'before_insert')
def set_fund_id(mapper, connection, target):
    # id가 이미 설정되어 있지 않은 경우에만 자동 생성
    if target.id is None or target.id == '':
        target.id = generate_fund_id({'get_bind': lambda: connection})
