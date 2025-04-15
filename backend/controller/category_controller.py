"""
카테고리 관련 API 엔드포인트를 정의하는 라우터
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.database import get_db
from backend.service import category_service
from backend.schemas.category import CategoryCreate, Category, CategoryUpdate
from backend.middleware.auth import jwt_bearer

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(jwt_bearer)]  # 모든 카테고리 엔드포인트에 JWT 인증 적용
)

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    새로운 카테고리를 생성합니다.
    """
    return category_service.create_category(db=db, category=category)

@router.get("/{category_id}", response_model=Category)
def read_category(category_id: str, db: Session = Depends(get_db)):
    """
    특정 카테고리를 조회합니다.
    """
    db_category = category_service.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: str, category: CategoryUpdate, db: Session = Depends(get_db)):
    """
    카테고리 정보를 업데이트합니다.
    """
    db_category = category_service.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    return db_category

@router.delete("/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """
    카테고리를 삭제합니다.
    """
    success = category_service.delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    return {"message": "카테고리가 성공적으로 삭제되었습니다"}
