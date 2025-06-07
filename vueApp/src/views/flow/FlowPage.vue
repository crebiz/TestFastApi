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
            플로우 다이어그램
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="resetFlow">초기화</v-btn>
          </v-card-title>
          
          <!-- 탭 메뉴 추가 -->
          <v-tabs v-model="activeTab" bg-color="primary">
            <v-tab value="recipe">김치찌개 레시피 플로우</v-tab>
            <v-tab value="mindmap">마인드맵 플로우</v-tab>
          </v-tabs>
          
          <v-card-text>
            <v-window v-model="activeTab">
              <!-- 레시피 플로우 탭 -->
              <v-window-item value="recipe">
                <div class="flow-wrapper">
                  <!-- 노드 사이드바 컴포넌트 -->
                  <NodeSidebar />
                  
                  <!-- Vue Flow 캔버스 -->
                  <div class="flow-container">
                    <VueFlow
                      v-model="elements"
                      :default-zoom="1.5"
                      :min-zoom="0.5"
                      :max-zoom="2"
                      :node-types="nodeTypes"
                      class="flow-canvas"
                      :default-edge-options="defaultEdgeOptions"
                      :connection-line-style="connectionLineStyle"
                      @connect="onConnect"
                      @dragover="onDragOver"
                      @drop="onDrop"
                      @edge-update="onEdgeUpdate"
                      @edge-update-end="onEdgeUpdateEnd"
                >
                  <Background pattern-color="#aaa" gap="8" />
                  <MiniMap />
                  <Controls />
                  <Panel position="top-right" class="legend">
                    <div class="legend-title">노드 유형</div>
                    <div class="legend-item">
                      <div class="legend-color input-node"></div>
                      <div>재료</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color default-node"></div>
                      <div>조리 과정</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color output-node"></div>
                      <div>완성</div>
                    </div>
                    <div class="legend-item">
                      <div class="legend-color seasoning-node"></div>
                      <div>양념</div>
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
              </v-window-item>
              
              <!-- 마인드맵 플로우 탭 -->
              <v-window-item value="mindmap">
                <MindMapFlow />
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { VueFlow, useVueFlow, Panel } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { MarkerType } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

// 마인드맵 컴포넌트 가져오기
import MindMapFlow from './MindMapFlow.vue'

// 커스텀 컴포넌트 가져오기
import NodeSidebar from './components/NodeSidebar.vue'
import CustomNode from './components/CustomNode.vue'
import NodeDetailDrawer from './components/NodeDetailDrawer.vue'

// 노드 타입 정의
const nodeTypes = {
  custom: CustomNode
}

// Vue Flow 훅 사용
const { addEdges, addNodes, project } = useVueFlow()

// 연결 유효성 검사 옵션
const connectionLineStyle = { stroke: '#555', strokeWidth: 2 }
const defaultEdgeOptions = {
  type: 'smoothstep',
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
  // 재료 노드 (Input Nodes)
  { id: '1', type: 'input', data: { label: '🐷 돼지고기 (목살 300g)\n(한입 크기)' }, position: { x: 50, y: 0 }, class: 'input-node' },
  { id: '2', type: 'input', data: { label: '🥬 김치 (1/4포기 400g)\n(먹기 좋게)' }, position: { x: 50, y: 100 }, class: 'input-node' },
  { id: '3', type: 'input', data: { label: '🧅 양파 (1/2개)\n(채 썰기)' }, position: { x: 50, y: 200 }, class: 'input-node' },
  { id: '4', type: 'input', data: { label: '🌿 대파 (1/2대)\n(어슷 썰기)' }, position: { x: 50, y: 300 }, class: 'input-node' },
  { id: '5', type: 'input', data: { label: '⬜ 두부 (1/2모)\n(적당히 썰기)' }, position: { x: 50, y: 400 }, class: 'input-node' },
  { id: '6', type: 'input', data: { label: '🌶️ 고추 (청양/홍 1개씩)\n(어슷 썰기)' }, position: { x: 50, y: 500 }, class: 'input-node' },
  { id: '7', type: 'input', data: { label: '💧 멸치 다시마 육수 (600ml)' }, position: { x: 50, y: 600 }, class: 'input-node' },

  // 양념장 노드 (Default Nodes)
  { id: '8', type: 'default', data: { label: '🌶️ 고춧가루 (2.5T)' }, position: { x: 300, y: 0 }, class: 'seasoning-node' },
  { id: '9', type: 'default', data: { label: '🥣 국간장 (2T)' }, position: { x: 300, y: 70 }, class: 'seasoning-node' },
  { id: '10', type: 'default', data: { label: '🧄 다진 마늘 (1.5T)' }, position: { x: 300, y: 140 }, class: 'seasoning-node' },
  { id: '11', type: 'default', data: { label: '🤎 된장 (0.5T)' }, position: { x: 300, y: 210 }, class: 'seasoning-node' },
  { id: '12', type: 'default', data: { label: '🍚 설탕 (0.5T)' }, position: { x: 300, y: 280 }, class: 'seasoning-node' },
  { id: '15', type: 'default', data: { label: '🥄 양념장 만들기\n(8+9+10+11+12)' }, position: { x: 550, y: 140 }, class: 'default-node' },

  // 조리 과정 노드 (Default Nodes)
  { id: '13', type: 'default', data: { label: '🥓 돼지고기 볶기' }, position: { x: 550, y: 350 }, class: 'default-node' },
  { id: '14', type: 'default', data: { label: '🥬 김치 넣고 볶기' }, position: { x: 550, y: 450 }, class: 'default-node' },
  { id: '16', type: 'default', data: { label: '🍲 육수 및 양념장 투입' }, position: { x: 800, y: 400 }, class: 'default-node' },
  { id: '17', type: 'default', data: { label: '🔥 10분간 끓이기' }, position: { x: 800, y: 500 }, class: 'default-node' },
  { id: '18', type: 'default', data: { label: '🧅 채소 및 두부 투입' }, position: { x: 1050, y: 500 }, class: 'default-node' },
  { id: '19', type: 'default', data: { label: '♨️ 5분 더 끓이기' }, position: { x: 1300, y: 500 }, class: 'default-node' },

  // 완성 노드 (Output Node)
  { id: '20', type: 'output', data: { label: '✅ 김치찌개 완성!' }, position: { x: 1550, y: 500 }, class: 'output-node' },
]

// 초기 엣지 정의
const initialEdges = [
  // 재료 -> 조리
  { id: 'e1-13', source: '1', target: '13', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 돼지고기 -> 돼지고기 볶기
  { id: 'e2-14', source: '2', target: '14', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 김치 -> 김치 볶기

  // 양념장 재료 -> 양념장 만들기
  { id: 'e8-15', source: '8', target: '15', animated: true },
  { id: 'e9-15', source: '9', target: '15', animated: true },
  { id: 'e10-15', source: '10', target: '15', animated: true },
  { id: 'e11-15', source: '11', target: '15', animated: true },
  { id: 'e12-15', source: '12', target: '15', animated: true },

  // 조리 과정 순서
  { id: 'e13-14', source: '13', target: '14', animated: true, label: '반쯤 익으면', labelBgStyle: { fill: '#E1F5FE' } }, // 돼지고기 볶기 -> 김치 볶기
  { id: 'e14-16', source: '14', target: '16', animated: true, label: '김치가 부드러워지면', labelBgStyle: { fill: '#E1F5FE' } }, // 김치 볶기 -> 육수+양념장
  { id: 'e15-16', source: '15', target: '16', animated: true, label: '양념장 준비', labelBgStyle: { fill: '#E8F5E9' } }, // 양념장 만들기 -> 육수+양념장 투입
  { id: 'e7-16', source: '7', target: '16', animated: true, label: '육수 준비', labelBgStyle: { fill: '#E8F5E9' } }, // 육수 -> 육수+양념장 투입

  { id: 'e16-17', source: '16', target: '17', animated: true, label: '투입 후', labelBgStyle: { fill: '#E1F5FE' } }, // 육수+양념장 투입 -> 10분 끓이기
  { id: 'e17-18', source: '17', target: '18', animated: true, label: '10분 후', labelBgStyle: { fill: '#E1F5FE' } }, // 10분 끓이기 -> 채소/두부 투입

  // 채소/두부 투입
  { id: 'e3-18', source: '3', target: '18', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 양파 -> 채소/두부 투입
  { id: 'e4-18', source: '4', target: '18', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 대파 -> 채소/두부 투입
  { id: 'e5-18', source: '5', target: '18', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 두부 -> 채소/두부 투입
  { id: 'e6-18', source: '6', target: '18', animated: true, label: '재료준비', labelBgStyle: { fill: '#FFCDD2' } }, // 고추 -> 채소/두부 투입

  { id: 'e18-19', source: '18', target: '19', animated: true, label: '투입 후', labelBgStyle: { fill: '#E1F5FE' } }, // 채소/두부 투입 -> 5분 더 끓이기
  { id: 'e19-20', source: '19', target: '20', animated: true, label: '5분 후', labelBgStyle: { fill: '#E1F5FE' } }, // 5분 더 끓이기 -> 완성
]

const elements = ref([])

// 노드 상세 드로어 관련 상태
const isDrawerOpen = ref(false)
const selectedNodeId = ref('')
const selectedNodeData = ref<any>({})

// 노드 ID 카운터
let nodeIdCounter = 0

// 활성 탭
const activeTab = ref('recipe')

// 김치찌개 레시피 플로우 요소 설정
function fetchFlowElements() {
  try {
    // 백엔드 API 호출 대신 초기 데이터 사용
    elements.value = [...initialNodes, ...initialEdges]
    console.log('김치찌개 레시피 플로우 데이터 로드 완료')
  } catch (error) {
    console.error('플로우 데이터를 설정하는 중 오류 발생:', error)
  }
}

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  fetchFlowElements()
})

// 연결 이벤트 핸들러
const onConnect = (params: any) => {
  // 자기 자신에게 연결하는 것 방지
  if (params.source === params.target) {
    console.warn('노드를 자기 자신에게 연결할 수 없습니다.')
    return
  }
  
  // 이미 존재하는 연결인지 확인
  const edgeExists = elements.value.some(
    (el: any) => el.id === `e${params.source}-${params.target}`
  )
  
  if (edgeExists) {
    console.warn('이미 연결이 존재합니다.')
    return
  }
  
  // 새 엣지 추가
  const newEdge = {
    id: `e${params.source}-${params.target}`,
    ...params,
    animated: true,
    style: { stroke: '#555', strokeWidth: 2 },
    label: '연결됨',
    labelBgStyle: { fill: '#FFFFFF', fillOpacity: 0.7 },
    labelStyle: { fill: '#333333', fontSize: 12 }
  }
  
  addEdges([newEdge])
  
  // 백엔드에 연결 정보 저장 (필요한 경우)
  // saveEdgeToBackend(newEdge)
}

// 엣지 업데이트 핸들러 (엣지 드래그 중)
const onEdgeUpdate = (oldEdge: any, newConnection: any) => {
  // 이전 엣지 제거 및 새 연결 추가
  const edgeIndex = elements.value.findIndex((el: any) => el.id === oldEdge.id)
  if (edgeIndex !== -1) {
    elements.value.splice(edgeIndex, 1)
  }
  
  // 새 연결 생성
  onConnect({
    source: newConnection.source || oldEdge.source,
    sourceHandle: newConnection.sourceHandle || oldEdge.sourceHandle,
    target: newConnection.target || oldEdge.target,
    targetHandle: newConnection.targetHandle || oldEdge.targetHandle
  })
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
  
  if (nodeType === 'sample-node-1') {
    label = '샘플노드1'
    description = '이것은 샘플노드1입니다'
  } else if (nodeType === 'sample-node-2') {
    label = '샘플노드2'
    description = '이것은 샘플노드2입니다'
  } else if (nodeType === 'sample-node-3') {
    label = '샘플노드3'
    description = '이것은 샘플노드3입니다'
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
    }
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
  const { updateNode } = useVueFlow()
  updateNode(nodeId, { data: updatedData })
  
  // 업데이트된 노드 찾기
  const nodeIndex = elements.value.findIndex((el: any) => el.id === nodeId)
  if (nodeIndex !== -1) {
    elements.value[nodeIndex].data = updatedData
  }
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
.input-node {
}

.default-node {
}

.output-node {
}

.seasoning-node {
}



/* 범례 스타일 */
.legend {
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

.legend-color.input-node {
  background-color: var(--color-background);
  border: 1px solid var(--color-primary);
}

.legend-color.default-node {
  background-color: var(--color-tertiary);
  border: 1px solid var(--text-on-tertiary);
}

.legend-color.output-node {
  background-color: var(--color-secondary);
  border: 1px solid var(--text-on-secondary);
}

.legend-color.seasoning-node {
  background-color: var(--color-primary);
  border: 1px solid var(--text-on-primary);
}
</style>