from typing import List
from sqlalchemy.orm import Session
from backend.model.fund import Fund
from backend.schemas.fund import FundCreate


class FundService:

  @staticmethod
  def create_fund(db: Session, fund: FundCreate) -> Fund:
      db_fund = Fund(
        id=fund.id,
        financial_comp=fund.financial_comp,
        type=fund.type,
        account_num=fund.account_num,
        fund_nm=fund.fund_nm
      )

      db.add(db_fund)
      db.commit()
      db.refresh(db_fund)

      return db_fund
  
  @staticmethod
  def get_funds(db: Session, skip: int = 0, limit: int = 100) -> List[Fund]:
      return db.query(Fund).offset(skip).limit(limit).all()