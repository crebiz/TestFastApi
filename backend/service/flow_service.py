from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ..model.flow import FlowNode, FlowEdge
from ..schemas.flow import FlowNodeCreate, FlowEdgeCreate

class FlowService:
    def create_node(self, db: Session, node: FlowNodeCreate):
        db_node = FlowNode(
            id=node.id,
            type=node.type,
            position_x=node.position_x,
            position_y=node.position_y,
            label=node.label,
            description=node.description,
            node_type=node.node_type
        )
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node
    
    def create_edge(self, db: Session, edge: FlowEdgeCreate):
        db_edge = FlowEdge(
            id=edge.id,
            source=edge.source,
            target=edge.target,
            animated=edge.animated
        )
        db.add(db_edge)
        db.commit()
        db.refresh(db_edge)
        return db_edge
    
    def get_all_nodes(self, db: Session):
        return db.query(FlowNode).all()
    
    def get_all_edges(self, db: Session):
        return db.query(FlowEdge).all()
    
    def get_node_by_id(self, db: Session, node_id: str):
        return db.query(FlowNode).filter(FlowNode.id == node_id).first()
    
    def get_edge_by_id(self, db: Session, edge_id: str):
        return db.query(FlowEdge).filter(FlowEdge.id == edge_id).first()
    
    def update_node(self, db: Session, node_id: str, node_data: Dict[str, Any]):
        db_node = self.get_node_by_id(db, node_id)
        if db_node:
            for key, value in node_data.items():
                if hasattr(db_node, key):
                    setattr(db_node, key, value)
            db.commit()
            db.refresh(db_node)
        return db_node
    
    def update_edge(self, db: Session, edge_id: str, edge_data: Dict[str, Any]):
        db_edge = self.get_edge_by_id(db, edge_id)
        if db_edge:
            for key, value in edge_data.items():
                if hasattr(db_edge, key):
                    setattr(db_edge, key, value)
            db.commit()
            db.refresh(db_edge)
        return db_edge
    
    def delete_node(self, db: Session, node_id: str):
        db_node = self.get_node_by_id(db, node_id)
        if db_node:
            db.delete(db_node)
            db.commit()
            return True
        return False
    
    def delete_edge(self, db: Session, edge_id: str):
        db_edge = self.get_edge_by_id(db, edge_id)
        if db_edge:
            db.delete(db_edge)
            db.commit()
            return True
        return False
    
    def get_all_elements(self, db: Session) -> List[Dict[str, Any]]:
        """모든 노드와 엣지를 가져와서 프론트엔드에 맞는 형식으로 변환"""
        nodes = self.get_all_nodes(db)
        edges = self.get_all_edges(db)
        
        # 프론트엔드 형식으로 변환
        return self.convert_to_frontend_format(nodes, edges)
    
    def convert_to_frontend_format(self, nodes, edges):
        """DB 모델을 프론트엔드 Vue Flow 형식으로 변환"""
        elements = []
        
        # 노드 변환
        for node in nodes:
            elements.append({
                'id': node.id,
                'type': node.type,
                'position': {'x': node.position_x, 'y': node.position_y},
                'data': {
                    'label': node.label,
                    'description': node.description,
                    'type': node.node_type
                }
            })
        
        # 엣지 변환
        for edge in edges:
            elements.append({
                'id': edge.id,
                'source': edge.source,
                'target': edge.target,
                'animated': edge.animated
            })
        
        return elements
