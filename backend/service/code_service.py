from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.model.code import CodeGroup, CodeDetail
from backend.schemas.code import CodeGroupCreate, CodeGroupUpdate, CodeDetailCreate, CodeDetailUpdate


class CodeService:
    @staticmethod
    def get_code_groups(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None):
        query = db.query(CodeGroup)
        if is_active is not None:
            query = query.filter(CodeGroup.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_code_group(db: Session, group_id: str):
        return db.query(CodeGroup).filter(CodeGroup.id == group_id).first()

    @staticmethod
    def create_code_group(db: Session, code_group: CodeGroupCreate):
        db_code_group = CodeGroup(
            id=code_group.id,
            name=code_group.name,
            description=code_group.description,
            is_active=code_group.is_active
        )
        db.add(db_code_group)
        db.commit()
        db.refresh(db_code_group)
        return db_code_group

    @staticmethod
    def update_code_group(db: Session, group_id: str, code_group: CodeGroupUpdate):
        db_code_group = db.query(CodeGroup).filter(CodeGroup.id == group_id).first()
        if db_code_group:
            update_data = code_group.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_code_group, key, value)
            db_code_group.updated_at = datetime.now()
            db.commit()
            db.refresh(db_code_group)
        return db_code_group

    @staticmethod
    def delete_code_group(db: Session, group_id: str):
        db_code_group = db.query(CodeGroup).filter(CodeGroup.id == group_id).first()
        if db_code_group:
            db.delete(db_code_group)
            db.commit()
            return True
        return False

    @staticmethod
    def get_code_details(db: Session, group_id: Optional[str] = None, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None):
        query = db.query(CodeDetail)
        if group_id:
            query = query.filter(CodeDetail.group_id == group_id)
        if is_active is not None:
            query = query.filter(CodeDetail.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_code_detail(db: Session, detail_id: str):
        return db.query(CodeDetail).filter(CodeDetail.id == detail_id).first()

    @staticmethod
    def create_code_detail(db: Session, code_detail: CodeDetailCreate):
        db_code_detail = CodeDetail(
            id=code_detail.id,
            group_id=code_detail.group_id,
            name=code_detail.name,
            value=code_detail.value,
            description=code_detail.description,
            sort_order=code_detail.sort_order,
            is_active=code_detail.is_active
        )
        db.add(db_code_detail)
        db.commit()
        db.refresh(db_code_detail)
        return db_code_detail

    @staticmethod
    def update_code_detail(db: Session, detail_id: str, code_detail: CodeDetailUpdate):
        db_code_detail = db.query(CodeDetail).filter(CodeDetail.id == detail_id).first()
        if db_code_detail:
            update_data = code_detail.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_code_detail, key, value)
            db_code_detail.updated_at = datetime.now()
            db.commit()
            db.refresh(db_code_detail)
        return db_code_detail

    @staticmethod
    def delete_code_detail(db: Session, detail_id: str):
        db_code_detail = db.query(CodeDetail).filter(CodeDetail.id == detail_id).first()
        if db_code_detail:
            db.delete(db_code_detail)
            db.commit()
            return True
        return False
