
# 로깅 설정
import logging
import os
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.schemas.fund import Fund, FundCreate, FundUpdate
from backend.service.fund_service import FundService


log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('fund_controller')
logger.setLevel(logging.INFO)

# 파일 핸들러 설정
log_file = os.path.join(log_dir, 'fund_controller.log')
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

# API 라우터 설정
router = APIRouter(
    prefix="/funds",  # URL 접두사
    tags=["funds"]    # Swagger 문서 태그
)

@router.post("/", response_model=Fund)
def create_fund(fund: FundCreate, db: Session = Depends(get_db)):
    return FundService.create_fund(db=db, fund=fund)

@router.get("/total", response_model=List[Fund])
def read_funds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return FundService.get_total_funds(db=db, skip=skip, limit=limit)

@router.get("/", response_model=List[Fund])
def read_funds(type: Optional[str] = Query(None), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return FundService.get_funds(db=db, skip=skip, limit=limit, type=type)

@router.put("/{fund_id}/toggle-state", response_model=Fund)
def toggle_fund_state(fund_id: str, db: Session = Depends(get_db)):
    """펀드 상태를 active <-> inactive로 토글합니다."""
    logger.info(f"Toggling state for fund {fund_id}")
    try:
        return FundService.toggle_fund_state(db=db, fund_id=fund_id)
    except ValueError as e:
        logger.error(f"Error toggling fund state: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{fund_id}", response_model=Fund)
def update_fund(fund_id: str, fund: FundUpdate, db: Session = Depends(get_db)):
    """펀드 정보를 업데이트합니다."""
    logger.info(f"Updating fund {fund_id}")
    try:
        # Pydantic 모델을 dict로 변환하고 None 값은 제외
        fund_data = {k: v for k, v in fund.dict().items() if v is not None}
        return FundService.update_fund(db=db, fund_id=fund_id, fund_data=fund_data)
    except ValueError as e:
        logger.error(f"Error updating fund: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))