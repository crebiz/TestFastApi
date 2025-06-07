from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database.database import get_db
from ..service.flow_service import FlowService
from ..schemas.flow import FlowNodeCreate, FlowEdgeCreate, FlowNodeResponse, FlowEdgeResponse

router = APIRouter(
    prefix="/api/flows",
    tags=["flows"],
    responses={404: {"description": "Not found"}},
)

flow_service = FlowService()

@router.get("/elements", response_model=List[Dict[str, Any]])
def get_flow_elements(db: Session = Depends(get_db)):
    """모든 플로우 요소(노드와 엣지)를 가져옵니다."""
    nodes = flow_service.get_all_nodes(db)
    edges = flow_service.get_all_edges(db)
    
    # 프론트엔드 형식으로 변환
    elements = flow_service.convert_to_frontend_format(nodes, edges)
    return elements

@router.post("/nodes", response_model=FlowNodeResponse)
def create_node(node: FlowNodeCreate, db: Session = Depends(get_db)):
    """새로운 노드를 생성합니다."""
    return flow_service.create_node(db, node)

@router.post("/edges", response_model=FlowEdgeResponse)
def create_edge(edge: FlowEdgeCreate, db: Session = Depends(get_db)):
    """새로운 엣지를 생성합니다."""
    return flow_service.create_edge(db, edge)

@router.get("/nodes", response_model=List[FlowNodeResponse])
def get_all_nodes(db: Session = Depends(get_db)):
    """모든 노드를 가져옵니다."""
    return flow_service.get_all_nodes(db)

@router.get("/edges", response_model=List[FlowEdgeResponse])
def get_all_edges(db: Session = Depends(get_db)):
    """모든 엣지를 가져옵니다."""
    return flow_service.get_all_edges(db)

@router.get("/nodes/{node_id}", response_model=FlowNodeResponse)
def get_node(node_id: str, db: Session = Depends(get_db)):
    """특정 ID의 노드를 가져옵니다."""
    node = flow_service.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.get("/edges/{edge_id}", response_model=FlowEdgeResponse)
def get_edge(edge_id: str, db: Session = Depends(get_db)):
    """특정 ID의 엣지를 가져옵니다."""
    edge = flow_service.get_edge_by_id(db, edge_id)
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    return edge

@router.put("/nodes/{node_id}", response_model=FlowNodeResponse)
def update_node(node_id: str, node_data: Dict[str, Any], db: Session = Depends(get_db)):
    """노드를 업데이트합니다."""
    updated_node = flow_service.update_node(db, node_id, node_data)
    if not updated_node:
        raise HTTPException(status_code=404, detail="Node not found")
    return updated_node

@router.put("/edges/{edge_id}", response_model=FlowEdgeResponse)
def update_edge(edge_id: str, edge_data: Dict[str, Any], db: Session = Depends(get_db)):
    """엣지를 업데이트합니다."""
    updated_edge = flow_service.update_edge(db, edge_id, edge_data)
    if not updated_edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    return updated_edge

@router.delete("/nodes/{node_id}")
def delete_node(node_id: str, db: Session = Depends(get_db)):
    """노드를 삭제합니다."""
    success = flow_service.delete_node(db, node_id)
    if not success:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Node deleted successfully"}

@router.delete("/edges/{edge_id}")
def delete_edge(edge_id: str, db: Session = Depends(get_db)):
    """엣지를 삭제합니다."""
    success = flow_service.delete_edge(db, edge_id)
    if not success:
        raise HTTPException(status_code=404, detail="Edge not found")
    return {"message": "Edge deleted successfully"}
