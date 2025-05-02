import logging
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.schemas.card import Card, CardCreate, CardUpdate
from backend.schemas.card_statistics import CardStatistics, MonthlyStat
from backend.service.card_service import CardService

# 로깅 설정
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('card_controller')
logger.setLevel(logging.INFO)

# 파일 핸들러 설정
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

# API 라우터 설정
router = APIRouter(
    prefix="/cards",  # URL 접두사
    tags=["cards"]    # Swagger 문서 태그
)


@router.get("/statistics", response_model=CardStatistics)
def get_card_statistics(
    card_code: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    카드 사용내역 통계 조회
    
    - **card_code**: 카드 코드로 필터링 (예: 'SH', 'LT', 'SS')
    - **year**: 연도로 필터링 (예: 2025)
    - **month**: 월로 필터링 (예: 1-12)
    """
    logger.info(f"카드 사용내역 통계 조회: card_code={card_code}, year={year}, month={month}")
    statistics = CardService.get_card_statistics(db, card_code=card_code, year=year, month=month)
    return statistics


@router.get("/all-monthly-stats", response_model=List[MonthlyStat])
def get_all_monthly_stats(db: Session = Depends(get_db)):
    """
    전체 데이터의 월별 통계 조회 (선택한 월과 상관없이 전체 데이터 기반)
    """
    logger.info("전체 데이터의 월별 통계 조회")
    monthly_stats = CardService.get_all_monthly_stats(db)
    return monthly_stats


@router.get("/", response_model=List[Card])
def get_cards(
    skip: int = 0, 
    limit: int = 200, 
    card_code: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    카드 사용내역 목록 조회
    
    - **skip**: 건너뛸 레코드 수
    - **limit**: 최대 조회 레코드 수
    - **card_code**: 카드 코드로 필터링 (예: 'SH', 'LT', 'SS')
    - **category**: 분류로 필터링 (예: '식비', '교통', '쇼핑')
    - **year**: 연도로 필터링 (예: 2025)
    - **month**: 월로 필터링 (예: 1-12)
    """
    logger.info(f"카드 사용내역 목록 조회: skip={skip}, limit={limit}, card_code={card_code}, category={category}, year={year}, month={month}")
    cards = CardService.get_cards(db, skip=skip, limit=limit, card_code=card_code, category=category, year=year, month=month)
    return cards


@router.get("/{card_id}", response_model=Card)
def get_card(card_id: str, db: Session = Depends(get_db)):
    """
    카드 사용내역 상세 조회
    
    - **card_id**: 카드 사용내역 ID
    """
    logger.info(f"카드 사용내역 상세 조회: card_id={card_id}")
    db_card = CardService.get_card(db, card_id=card_id)
    if db_card is None:
        logger.warning(f"카드 사용내역 없음: card_id={card_id}")
        raise HTTPException(status_code=404, detail="카드 사용내역을 찾을 수 없습니다")
    return db_card


@router.post("/", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    """
    카드 사용내역 생성
    
    - **card**: 생성할 카드 사용내역 정보
    """
    logger.info(f"카드 사용내역 생성: {card.dict()}")
    return CardService.create_card(db=db, card=card)


@router.put("/{card_id}", response_model=Card)
def update_card(card_id: str, card: CardUpdate, db: Session = Depends(get_db)):
    """
    카드 사용내역 수정
    
    - **card_id**: 수정할 카드 사용내역 ID
    - **card**: 수정할 내용
    """
    logger.info(f"카드 사용내역 수정: card_id={card_id}, data={card.dict()}")
    db_card = CardService.update_card(db, card_id=card_id, card=card)
    if db_card is None:
        logger.warning(f"카드 사용내역 없음: card_id={card_id}")
        raise HTTPException(status_code=404, detail="카드 사용내역을 찾을 수 없습니다")
    return db_card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: str, db: Session = Depends(get_db)):
    """
    카드 사용내역 삭제
    
    - **card_id**: 삭제할 카드 사용내역 ID
    """
    logger.info(f"카드 사용내역 삭제: card_id={card_id}")
    result = CardService.delete_card(db, card_id=card_id)
    if not result:
        logger.warning(f"카드 사용내역 없음: card_id={card_id}")
        raise HTTPException(status_code=404, detail="카드 사용내역을 찾을 수 없습니다")


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_excel(
    file: UploadFile = File(...),
    year: int = Form(...),
    month: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    엑셀 파일 업로드를 통한 카드 사용내역 일괄 생성
    
    - **file**: 업로드할 엑셀 파일 (.xlsx, .xls)
    - **card_code**: (선택사항) 카드 코드. 지정하지 않으면 엑셀 파일에서 자동 추출
    """
    logger.info(f"카드 사용내역 엑셀 업로드: filename={file.filename}, year={year}, month={month}")
    
    # 파일 확장자 검증
    if not file.filename.endswith(('.xlsx', '.xls')):
        logger.warning(f"잘못된 파일 형식: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="엑셀 파일(.xlsx, .xls)만 업로드 가능합니다."
        )
    
    try:
        # 파일 내용 읽기
        contents = await file.read()
        use_month = f"{year}{month:02d}"
        
        # 엑셀 파일 처리
        result = CardService.process_excel_file(db, contents, use_month=use_month)
        
        logger.info(f"엑셀 파일 처리 완료: {result}")
        return {
            "message": "엑셀 파일 처리 완료",
            "filename": file.filename,
            "result": result
        }
        
    except ValueError as e:
        logger.error(f"엑셀 파일 처리 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"서버 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="파일 처리 중 서버 오류가 발생했습니다."
        )
    finally:
        # 파일 닫기
        await file.close()
