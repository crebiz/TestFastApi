from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict, Any, Union, Annotated
from datetime import datetime

class Position(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    label: str
    description: Optional[str] = None
    type: str

class NodeBase(BaseModel):
    id: str
    type: str
    position: Position
    data: NodeData

class EdgeBase(BaseModel):
    id: str
    source: str
    target: str
    animated: Optional[bool] = False

# 아래 클래스들은 현재 사용되지 않음
# class FlowElement(RootModel):
#     root: Union[NodeBase, EdgeBase]

# class FlowElementList(RootModel):
#     root: List[Union[NodeBase, EdgeBase]]

# DB 모델과 연동되는 스키마
class FlowNodeCreate(BaseModel):
    id: str
    type: str
    position_x: float
    position_y: float
    label: str
    description: Optional[str] = None
    node_type: str

class FlowNodeResponse(FlowNodeCreate):
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class FlowEdgeCreate(BaseModel):
    id: str
    source: str
    target: str
    animated: Optional[bool] = False

class FlowEdgeResponse(FlowEdgeCreate):
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

# 프론트엔드에 반환할 통합 스키마
class FlowElementResponse(BaseModel):
    nodes: List[FlowNodeResponse]
    edges: List[FlowEdgeResponse]
