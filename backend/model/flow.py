from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from ..database.database import Base
from ..utils.common import get_current_time

class FlowNode(Base):
    __tablename__ = "flow_nodes"
    
    id = Column(String(50), primary_key=True)
    type = Column(String(50), nullable=False)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    label = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    node_type = Column(String(50), nullable=False)  # data-source, preprocessing, model, evaluation, deployment
    created_at = Column(String(50), default=lambda: get_current_time(as_string=True))
    updated_at = Column(String(50), default=lambda: get_current_time(as_string=True), onupdate=lambda: get_current_time(as_string=True))
    
    # 노드에 연결된 엣지 (source로서)
    source_edges = relationship("FlowEdge", foreign_keys="FlowEdge.source", back_populates="source_node")
    # 노드에 연결된 엣지 (target으로서)
    target_edges = relationship("FlowEdge", foreign_keys="FlowEdge.target", back_populates="target_node")

class FlowEdge(Base):
    __tablename__ = "flow_edges"
    
    id = Column(String(50), primary_key=True)
    source = Column(String(50), ForeignKey("flow_nodes.id"), nullable=False)
    target = Column(String(50), ForeignKey("flow_nodes.id"), nullable=False)
    animated = Column(Boolean, default=False)
    created_at = Column(String(50), default=lambda: get_current_time(as_string=True))
    updated_at = Column(String(50), default=lambda: get_current_time(as_string=True), onupdate=lambda: get_current_time(as_string=True))
    
    # 관계 설정
    source_node = relationship("FlowNode", foreign_keys=[source], back_populates="source_edges")
    target_node = relationship("FlowNode", foreign_keys=[target], back_populates="target_edges")
