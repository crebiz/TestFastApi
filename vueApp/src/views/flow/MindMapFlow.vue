<template>
  <v-container fluid>
    <!-- 노드 상세 드로어 -->
    <NodeDetailDrawer
      v-model:isOpen="isDrawerOpen"
      :nodeId="selectedNodeId"
      :nodeData="selectedNodeData"
      @save="updateNodeData"
    />
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">
            마인드맵 플로우
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="resetFlow">초기화</v-btn>
            <v-btn color="success" class="ml-2" @click="addCentralNode">중앙 노드 추가</v-btn>
            <v-btn color="info" class="ml-2" @click="autoLayout">자동 배치</v-btn>
          </v-card-title>
          <v-card-text>
            <div class="flow-wrapper">
              <!-- 노드 사이드바 컴포넌트 -->
              <NodeSidebar />
              
              <!-- Vue Flow 캔버스 -->
              <div class="flow-container">
                <VueFlow
                  v-model="elements"
                  :default-zoom="1"
                  :min-zoom="0.2"
                  :max-zoom="4"
                  :node-types="nodeTypes"
                  class="flow-canvas"
                  :default-edge-options="defaultEdgeOptions"
                  :connection-line-style="connectionLineStyle"
                  @connect="onConnect"
                  @dragover="onDragOver"
                  @drop="onDrop"
                  @edge-update="onEdgeUpdate"
                  @edge-update-end="onEdgeUpdateEnd"
                  @node-double-click="onNodeDoubleClick"
                >
                  <Background pattern-color="#aaa" gap="8" />
                  <MiniMap />
                  <Controls />
                  <Panel position="top-right" class="legend">
                    <div class="legend-title">노드 유형</div>
                    <div class="legend-item">
                      <div class="legend-color central-node"></div>
                      <div>중앙 노드</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color main-node"></div>
                      <div>주요 개념</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color sub-node"></div>
                      <div>하위 개념</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color detail-node"></div>
                      <div>세부 사항</div>
                    </div>
                  </Panel>
                  
                  <template #node-custom="nodeProps">
                    <CustomNode 
                      :id="nodeProps.id" 
                      :data="nodeProps.data"
                      @dblclick="openNodeDetail(nodeProps.id, nodeProps.data)"
                    />
                  </template>
                </VueFlow>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { VueFlow, useVueFlow, Background, MiniMap, Controls, Panel } from '@vue-flow/core'
import { MarkerType } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

// 커스텀 컴포넌트 가져오기
import NodeSidebar from './components/NodeSidebar.vue'
import CustomNode from './components/CustomNode.vue'
import NodeDetailDrawer from './components/NodeDetailDrawer.vue'

// 노드 타입 정의
const nodeTypes = {
  custom: CustomNode
}

// Vue Flow 훅 사용
const { addEdges, addNodes, project, getNodes, getEdges, updateNode } = useVueFlow()

// 연결 유효성 검사 옵션
const connectionLineStyle = { stroke: '#555', strokeWidth: 2 }
const defaultEdgeOptions = {
  type: 'bezier', // 마인드맵에는 bezier 타입이 더 적합
  style: { strokeWidth: 2 },
  markerEnd: {
    type: MarkerType.ArrowClosed,
    width: 20,
    height: 20,
    color: '#888'
  },
  labelStyle: {
    fontSize: '12px',
    fontWeight: 'bold',
    fill: '#333'
  }
}

// 플로우 요소 저장 (노드 및 엣지)
// 초기 노드 정의
const initialNodes = [
  // 중앙 노드
  { 
    id: 'central', 
    type: 'custom', 
    data: { 
      label: '중앙 주제', 
      description: '마인드맵의 중심 주제입니다',
      type: 'central-node'
    }, 
    position: { x: 400, y: 300 }, 
    class: 'central-node' 
  },
  
  // 주요 개념 노드들
  { 
    id: 'main1', 
    type: 'custom', 
    data: { 
      label: '주요 개념 1', 
      description: '첫 번째 주요 개념입니다',
      type: 'main-node'
    }, 
    position: { x: 700, y: 150 }, 
    class: 'main-node' 
  },
  { 
    id: 'main2', 
    type: 'custom', 
    data: { 
      label: '주요 개념 2', 
      description: '두 번째 주요 개념입니다',
      type: 'main-node'
    }, 
    position: { x: 700, y: 450 }, 
    class: 'main-node' 
  },
  
  // 하위 개념 노드들
  { 
    id: 'sub1', 
    type: 'custom', 
    data: { 
      label: '하위 개념 1-1', 
      description: '첫 번째 주요 개념의 하위 개념입니다',
      type: 'sub-node'
    }, 
    position: { x: 950, y: 100 }, 
    class: 'sub-node' 
  },
  { 
    id: 'sub2', 
    type: 'custom', 
    data: { 
      label: '하위 개념 1-2', 
      description: '첫 번째 주요 개념의 또 다른 하위 개념입니다',
      type: 'sub-node'
    }, 
    position: { x: 950, y: 200 }, 
    class: 'sub-node' 
  },
  { 
    id: 'sub3', 
    type: 'custom', 
    data: { 
      label: '하위 개념 2-1', 
      description: '두 번째 주요 개념의 하위 개념입니다',
      type: 'sub-node'
    }, 
    position: { x: 950, y: 400 }, 
    class: 'sub-node' 
  },
  
  // 세부 사항 노드
  { 
    id: 'detail1', 
    type: 'custom', 
    data: { 
      label: '세부 사항 1-1-1', 
      description: '하위 개념 1-1의 세부 사항입니다',
      type: 'detail-node'
    }, 
    position: { x: 1200, y: 100 }, 
    class: 'detail-node' 
  }
]

// 초기 엣지 정의
const initialEdges = [
  // 중앙 노드에서 주요 개념으로의 연결
  { id: 'e-central-main1', source: 'central', target: 'main1', animated: false, label: '관계 1' },
  { id: 'e-central-main2', source: 'central', target: 'main2', animated: false, label: '관계 2' },
  
  // 주요 개념에서 하위 개념으로의 연결
  { id: 'e-main1-sub1', source: 'main1', target: 'sub1', animated: false, label: '세부' },
  { id: 'e-main1-sub2', source: 'main1', target: 'sub2', animated: false, label: '세부' },
  { id: 'e-main2-sub3', source: 'main2', target: 'sub3', animated: false, label: '세부' },
  
  // 하위 개념에서 세부 사항으로의 연결
  { id: 'e-sub1-detail1', source: 'sub1', target: 'detail1', animated: false, label: '상세' },
]

const elements = ref([])

// 노드 상세 드로어 관련 상태
const isDrawerOpen = ref(false)
const selectedNodeId = ref('')
const selectedNodeData = ref<any>({})

// 노드 ID 카운터
let nodeIdCounter = 0

// 마인드맵 요소 설정
function fetchFlowElements() {
  elements.value = [...initialNodes, ...initialEdges]
}

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  fetchFlowElements()
})

// 연결 이벤트 핸들러
const onConnect = (connection: any) => {
  // 연결 ID 생성
  const edgeId = `e-${connection.source}-${connection.target}`
  
  // 새 엣지 생성
  const newEdge = {
    id: edgeId,
    source: connection.source,
    target: connection.target,
    sourceHandle: connection.sourceHandle,
    targetHandle: connection.targetHandle,
    label: '관계',
    animated: false
  }
  
  // 엣지 추가
  addEdges([newEdge])
}

// 엣지 업데이트 핸들러
const onEdgeUpdate = (oldEdge: any, newConnection: any) => {
  addEdges([{
    id: oldEdge.id,
    source: newConnection.source || oldEdge.source,
    sourceHandle: newConnection.sourceHandle || oldEdge.sourceHandle,
    target: newConnection.target || oldEdge.target,
    targetHandle: newConnection.targetHandle || oldEdge.targetHandle
  }])
}

// 엣지 업데이트 완료 핸들러
const onEdgeUpdateEnd = (edge: any, success: boolean) => {
  if (success) {
    console.log('엣지 업데이트 성공:', edge)
  }
}

// 드래그 오버 이벤트 핸들러
const onDragOver = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
}

// 드롭 이벤트 핸들러
const onDrop = (event: DragEvent) => {
  event.preventDefault()
  
  if (!event.dataTransfer) return
  
  const nodeType = event.dataTransfer.getData('application/vueflow')
  
  // 드롭된 위치 계산
  const { left, top } = (event.target as HTMLElement).getBoundingClientRect()
  const position = project({
    x: event.clientX - left,
    y: event.clientY - top,
  })
  
  // 노드 타입별 설정
  const nodeId = `${nodeType}-${++nodeIdCounter}`
  let label = ''
  let description = ''
  let nodeClass = ''
  
  if (nodeType === 'central-node') {
    label = '중앙 주제'
    description = '마인드맵의 중심 주제입니다'
    nodeClass = 'central-node'
  } else if (nodeType === 'main-node') {
    label = '주요 개념'
    description = '주요 개념을 설명하세요'
    nodeClass = 'main-node'
  } else if (nodeType === 'sub-node') {
    label = '하위 개념'
    description = '하위 개념을 설명하세요'
    nodeClass = 'sub-node'
  } else if (nodeType === 'detail-node') {
    label = '세부 사항'
    description = '세부 사항을 설명하세요'
    nodeClass = 'detail-node'
  }
  
  // 새 노드 추가
  const newNode = {
    id: nodeId,
    type: 'custom',
    position,
    data: {
      label,
      description,
      type: nodeType
    },
    class: nodeClass
  }
  
  addNodes([newNode])
}

// 플로우 초기화 함수
const resetFlow = () => {
  elements.value = []
  setTimeout(() => {
    fetchFlowElements()
  }, 100)
}

// 노드 더블 클릭 이벤트 핸들러
const onNodeDoubleClick = (event: any, node: any) => {
  openNodeDetail(node.id, node.data)
}

// 노드 상세 정보 열기
const openNodeDetail = (nodeId: string, nodeData: any) => {
  console.log('노드 상세 정보 열기:', nodeId, nodeData)
  selectedNodeId.value = nodeId
  selectedNodeData.value = nodeData
  isDrawerOpen.value = true
}

// 노드 데이터 업데이트
const updateNodeData = (nodeId: string, updatedData: any) => {
  console.log('노드 데이터 업데이트:', nodeId, updatedData)
  
  // 노드 업데이트
  updateNode(nodeId, { data: updatedData })
  
  // 업데이트된 노드 찾기
  const nodeIndex = elements.value.findIndex((el: any) => el.id === nodeId)
  if (nodeIndex !== -1) {
    elements.value[nodeIndex].data = updatedData
  }
}

// 중앙 노드 추가
const addCentralNode = () => {
  const centralNodeId = `central-${++nodeIdCounter}`
  const position = { x: 400, y: 300 }
  
  const newNode = {
    id: centralNodeId,
    type: 'custom',
    position,
    data: {
      label: '새 중앙 주제',
      description: '새로운 마인드맵의 중심 주제입니다',
      type: 'central-node'
    },
    class: 'central-node'
  }
  
  addNodes([newNode])
}

// 자동 배치 함수
const autoLayout = () => {
  // 현재 노드와 엣지 가져오기
  const nodes = getNodes()
  const edges = getEdges()
  
  // 중앙 노드 찾기
  const centralNodes = nodes.filter(node => node.class === 'central-node')
  
  if (centralNodes.length === 0) return
  
  // 각 중앙 노드에 대해 연결된 노드 배치
  centralNodes.forEach(centralNode => {
    // 중앙 노드에 직접 연결된 노드 찾기
    const connectedMainNodes = edges
      .filter(edge => edge.source === centralNode.id)
      .map(edge => nodes.find(node => node.id === edge.target))
      .filter(Boolean)
    
    // 주요 개념 노드 주변에 방사형으로 배치
    const radius = 300
    const angleStep = (2 * Math.PI) / connectedMainNodes.length
    
    connectedMainNodes.forEach((mainNode, index) => {
      if (!mainNode) return
      
      const angle = index * angleStep
      const x = centralNode.position.x + radius * Math.cos(angle)
      const y = centralNode.position.y + radius * Math.sin(angle)
      
      // 주요 개념 노드 위치 업데이트
      updateNode(mainNode.id, { position: { x, y } })
      
      // 주요 개념 노드에 연결된 하위 노드 찾기
      const connectedSubNodes = edges
        .filter(edge => edge.source === mainNode.id)
        .map(edge => nodes.find(node => node.id === edge.target))
        .filter(Boolean)
      
      // 하위 노드 배치
      const subRadius = 150
      const subAngleStep = (Math.PI / 2) / (connectedSubNodes.length || 1)
      
      connectedSubNodes.forEach((subNode, subIndex) => {
        if (!subNode) return
        
        // 부모 노드 방향에서 약간 벌어진 각도로 배치
        const subAngle = angle - Math.PI / 4 + subIndex * subAngleStep
        const subX = x + subRadius * Math.cos(subAngle)
        const subY = y + subRadius * Math.sin(subAngle)
        
        // 하위 노드 위치 업데이트
        updateNode(subNode.id, { position: { x: subX, y: subY } })
        
        // 세부 사항 노드 찾기 및 배치
        const connectedDetailNodes = edges
          .filter(edge => edge.source === subNode.id)
          .map(edge => nodes.find(node => node.id === edge.target))
          .filter(Boolean)
        
        const detailRadius = 100
        connectedDetailNodes.forEach((detailNode, detailIndex) => {
          if (!detailNode) return
          
          const detailAngle = subAngle + (detailIndex - (connectedDetailNodes.length - 1) / 2) * 0.3
          const detailX = subX + detailRadius * Math.cos(detailAngle)
          const detailY = subY + detailRadius * Math.sin(detailAngle)
          
          // 세부 사항 노드 위치 업데이트
          updateNode(detailNode.id, { position: { x: detailX, y: detailY } })
        })
      })
    })
  })
}
</script>

<style scoped>
.flow-wrapper {
  display: flex;
  width: 100%;
  height: 800px;
}

.flow-container {
  flex-grow: 1;
  height: 100%;
}

.flow-canvas {
  width: 100%;
  height: 100%;
}

.custom-node {
  padding: 10px;
  border-radius: 5px;
  width: 180px;
  font-size: 12px;
  color: #222;
  text-align: center;
  border-width: 2px;
  border-style: solid;
}

.custom-node-header {
  font-weight: bold;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.custom-node-body {
  padding-top: 5px;
  font-size: 10px;
}

/* 노드 타입별 스타일 */
.central-node {
  background-color: #E8EAF6;
  border-color: #3F51B5;
  border-width: 3px;
  font-weight: bold;
}

.main-node {
  background-color: #E3F2FD;
  border-color: #2196F3;
}

.sub-node {
  background-color: #E1F5FE;
  border-color: #03A9F4;
}

.detail-node {
  background-color: #E0F7FA;
  border-color: #00BCD4;
}

/* 범례 스타일 */
.legend {
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.legend-title {
  font-weight: bold;
  margin-bottom: 8px;
  font-size: 14px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.legend-color {
  width: 15px;
  height: 15px;
  margin-right: 5px;
  border-radius: 3px;
}

.legend-color.central-node {
  background-color: #E8EAF6;
  border: 1px solid #3F51B5;
}

.legend-color.main-node {
  background-color: #E3F2FD;
  border: 1px solid #2196F3;
}

.legend-color.sub-node {
  background-color: #E1F5FE;
  border: 1px solid #03A9F4;
}

.legend-color.detail-node {
  background-color: #E0F7FA;
  border: 1px solid #00BCD4;
}
</style>
