from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database.database import get_db
from backend.service.code_service import CodeService
from backend.schemas.code import CodeGroup, CodeGroupCreate, CodeGroupUpdate, CodeDetail, CodeDetailCreate, CodeDetailUpdate
import logging
import os

# 로깅 설정
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('code_controller')
logger.setLevel(logging.INFO)

# 파일 핸들러 설정
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(log_dir, 'code_controller.log'),
    maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/codes",
    tags=["codes"],
    responses={404: {"description": "Not found"}},
)


# 그룹 코드 API 엔드포인트
@router.get("/groups", response_model=List[CodeGroup])
def get_code_groups(skip: int = 0, limit: int = 100, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    logger.info(f"그룹 코드 목록 조회: skip={skip}, limit={limit}, is_active={is_active}")
    code_groups = CodeService.get_code_groups(db, skip=skip, limit=limit, is_active=is_active)
    return code_groups


@router.get("/groups/{group_id}", response_model=CodeGroup)
def get_code_group(group_id: str, db: Session = Depends(get_db)):
    logger.info(f"그룹 코드 조회: group_id={group_id}")
    db_code_group = CodeService.get_code_group(db, group_id=group_id)
    if db_code_group is None:
        logger.warning(f"그룹 코드 없음: group_id={group_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="그룹 코드를 찾을 수 없습니다")
    return db_code_group


@router.post("/groups", response_model=CodeGroup, status_code=status.HTTP_201_CREATED)
def create_code_group(code_group: CodeGroupCreate, db: Session = Depends(get_db)):
    logger.info(f"그룹 코드 생성: {code_group.dict()}")
    db_code_group = CodeService.get_code_group(db, group_id=code_group.id)
    if db_code_group:
        logger.warning(f"그룹 코드 중복: group_id={code_group.id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 그룹 코드입니다")
    return CodeService.create_code_group(db=db, code_group=code_group)


@router.put("/groups/{group_id}", response_model=CodeGroup)
def update_code_group(group_id: str, code_group: CodeGroupUpdate, db: Session = Depends(get_db)):
    logger.info(f"그룹 코드 수정: group_id={group_id}, data={code_group.dict()}")
    db_code_group = CodeService.update_code_group(db, group_id=group_id, code_group=code_group)
    if db_code_group is None:
        logger.warning(f"그룹 코드 없음: group_id={group_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="그룹 코드를 찾을 수 없습니다")
    return db_code_group


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_code_group(group_id: str, db: Session = Depends(get_db)):
    logger.info(f"그룹 코드 삭제: group_id={group_id}")
    result = CodeService.delete_code_group(db, group_id=group_id)
    if not result:
        logger.warning(f"그룹 코드 없음: group_id={group_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="그룹 코드를 찾을 수 없습니다")


# 상세 코드 API 엔드포인트
@router.get("/details", response_model=List[CodeDetail])
def get_code_details(group_id: Optional[str] = None, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    logger.info(f"상세 코드 목록 조회: group_id={group_id}, skip={skip}, limit={limit}, is_active={is_active}")
    code_details = CodeService.get_code_details(db, group_id=group_id, skip=skip, limit=limit, is_active=is_active)
    return code_details


@router.get("/details/{detail_id}", response_model=CodeDetail)
def get_code_detail(detail_id: str, db: Session = Depends(get_db)):
    logger.info(f"상세 코드 조회: detail_id={detail_id}")
    db_code_detail = CodeService.get_code_detail(db, detail_id=detail_id)
    if db_code_detail is None:
        logger.warning(f"상세 코드 없음: detail_id={detail_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="상세 코드를 찾을 수 없습니다")
    return db_code_detail


@router.post("/details", response_model=CodeDetail, status_code=status.HTTP_201_CREATED)
def create_code_detail(code_detail: CodeDetailCreate, db: Session = Depends(get_db)):
    logger.info(f"상세 코드 생성: {code_detail.model_dump()}")
    # 그룹 코드 존재 여부 확인
    db_code_group = CodeService.get_code_group(db, group_id=code_detail.group_id)
    if not db_code_group:
        logger.warning(f"그룹 코드 없음: group_id={code_detail.group_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 그룹 코드입니다")
    
    # 상세 코드 ID 중복 확인
    db_code_detail = CodeService.get_code_detail(db, detail_id=code_detail.id)
    if db_code_detail:
        logger.warning(f"상세 코드 중복: detail_id={code_detail.id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 상세 코드입니다")
    
    return CodeService.create_code_detail(db=db, code_detail=code_detail)


@router.put("/details/{detail_id}", response_model=CodeDetail)
def update_code_detail(detail_id: str, code_detail: CodeDetailUpdate, db: Session = Depends(get_db)):
    logger.info(f"상세 코드 수정: detail_id={detail_id}, data={code_detail.model_dump()}")
    db_code_detail = CodeService.update_code_detail(db, detail_id=detail_id, code_detail=code_detail)
    if db_code_detail is None:
        logger.warning(f"상세 코드 없음: detail_id={detail_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="상세 코드를 찾을 수 없습니다")
    return db_code_detail


@router.delete("/details/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_code_detail(detail_id: str, db: Session = Depends(get_db)):
    logger.info(f"상세 코드 삭제: detail_id={detail_id}")
    result = CodeService.delete_code_detail(db, detail_id=detail_id)
    if not result:
        logger.warning(f"상세 코드 없음: detail_id={detail_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="상세 코드를 찾을 수 없습니다")
