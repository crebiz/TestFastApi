from sqlalchemy.orm import Session
from backend.model.category import Category
from backend.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate) -> Category:
    """
    새로운 카테고리를 생성합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        category (CategoryCreate): 생성할 카테고리 정보
    
    Returns:
        Category: 생성된 카테고리 객체
    """
    
    # 카테고리 객체 생성
    db_category = Category(
        id=category.id,
        name=category.name,
        parent_id=category.parent_id,
        fund=category.fund if category.fund else 0
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


def get_category(db: Session, category_id: str) -> Category:
    """
    카테고리 ID로 카테고리를 조회합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        category_id (str): 조회할 카테고리 ID
    
    Returns:
        Category: 조회된 카테고리 객체
    """
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category_id: str, category: CategoryUpdate) -> Category:
    """
    카테고리 정보를 업데이트합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        category_id (str): 업데이트할 카테고리 ID
        category (CategoryUpdate): 업데이트할 카테고리 정보
    
    Returns:
        Category: 업데이트된 카테고리 객체
    """
    db_category = get_category(db, category_id)
    if not db_category:
        return None
        
    # 업데이트할 필드만 반영
    if category.name is not None:
        db_category.name = category.name
    if category.parent_id is not None:
        db_category.parent_id = category.parent_id
    if category.fund is not None:
        db_category.fund = category.fund
        
    db.commit()
    db.refresh(db_category)
    
    return db_category


def delete_category(db: Session, category_id: str) -> bool:
    """
    카테고리를 삭제합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        category_id (str): 삭제할 카테고리 ID
    
    Returns:
        bool: 삭제 성공 여부
    """
    db_category = get_category(db, category_id)
    if not db_category:
        return False
        
    db.delete(db_category)
    db.commit()
    
    return True