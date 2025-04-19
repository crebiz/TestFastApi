from typing import List
from sqlalchemy.orm import Session
from backend.model.fund import Fund
from backend.schemas.fund import FundCreate


class FundService:
    """
    펀드 관리 서비스
    데이터베이스 작업과 비즈니스 로직을 처리합니다.
    """

    @staticmethod
    def create_fund(db: Session, fund: FundCreate) -> Fund:
        db_fund = Fund(
          # id는 자동 생성되므로 제거
          financial_comp=fund.financial_comp,
          type=fund.type,
          account_num=fund.account_num,
          fund_nm=fund.fund_nm,
          state=fund.state,
          invest_type=fund.invest_type,
          note=fund.note,
        )

        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)

        return db_fund
    
    @staticmethod
    def get_funds(db: Session, skip: int = 0, limit: int = 100, type: str = None) -> List[Fund]:
        query = db.query(Fund)
        if type:
            query = query.filter(Fund.type == type)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_total_funds(db: Session, skip: int = 0, limit: int = 100) -> List[Fund]:
        return db.query(Fund).offset(skip).limit(limit).all()
        
    @staticmethod
    def toggle_fund_state(db: Session, fund_id: str) -> Fund:
        """펀드 상태를 active <-> inactive로 토글합니다."""
        db_fund = db.query(Fund).filter(Fund.id == fund_id).first()
        if not db_fund:
            raise ValueError(f"Fund with id {fund_id} not found")
            
        # 상태 토글
        db_fund.state = "inactive" if db_fund.state == "active" else "active"
        
        db.commit()
        db.refresh(db_fund)
        return db_fund
        
    @staticmethod
    def update_fund(db: Session, fund_id: str, fund_data: dict) -> Fund:
        """펀드 정보를 업데이트합니다."""
        db_fund = db.query(Fund).filter(Fund.id == fund_id).first()
        if not db_fund:
            raise ValueError(f"Fund with id {fund_id} not found")
            
        # 업데이트 가능한 필드 목록
        updatable_fields = [
            "financial_comp", "type", "account_num", "fund_nm", 
            "state", "invest_type", "note"
        ]
        
        # 변경 사항 추적
        changes_made = False
        
        # 제공된 필드만 업데이트
        for field, value in fund_data.items():
            if field in updatable_fields and hasattr(db_fund, field):
                current_value = getattr(db_fund, field)
                if current_value != value:
                    setattr(db_fund, field, value)
                    changes_made = True
        
        # 변경 사항이 있을 경우에만 커밋
        if changes_made:
            db.commit()
            db.refresh(db_fund)
            
        return db_fund