from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from backend.database.database import Base
from backend.utils.common import get_current_time


class CodeGroup(Base):
    __tablename__ = "code_group"

    id = Column(String(10), primary_key=True)  # G001, G002 형식의 ID
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    sort_order = Column(String(10))  # 정렬 순서
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=lambda: get_current_time(as_string=True))  # 생성 시간
    updated_at = Column(String, default=lambda: get_current_time(as_string=True), onupdate=lambda: get_current_time(as_string=True))  # 수정 시간

    # 관계 설정 - 그룹코드에 속한 상세코드들
    details = relationship("CodeDetail", back_populates="group", cascade="all, delete-orphan")


class CodeDetail(Base):
    __tablename__ = "code_detail"

    id = Column(String(20), primary_key=True)  # 임의의 ID 값
    group_id = Column(String(10), ForeignKey("code_group.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(String(100))
    description = Column(String(255))
    sort_order = Column(String(10))  # 정렬 순서
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=lambda: get_current_time(as_string=True))  # 생성 시간
    updated_at = Column(String, default=lambda: get_current_time(as_string=True), onupdate=lambda: get_current_time(as_string=True))  # 수정 시간

    # 관계 설정 - 상세코드가 속한 그룹코드
    group = relationship("CodeGroup", back_populates="details")
