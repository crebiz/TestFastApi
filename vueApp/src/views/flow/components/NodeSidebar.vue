<template>
  <aside class="node-sidebar">
    <h3>노드 라이브러리</h3>
    <p class="sidebar-desc">노드를 드래그하여 캔버스에 추가하세요</p>
    
    <div
      class="dnd-node sample-node-1"
      draggable="true"
      @dragstart="onDragStart($event, 'sample-node-1')"
    >
      샘플노드1
    </div>
    
    <div
      class="dnd-node sample-node-2"
      draggable="true"
      @dragstart="onDragStart($event, 'sample-node-2')"
    >
      샘플노드2
    </div>
    
    <div
      class="dnd-node sample-node-3"
      draggable="true"
      @dragstart="onDragStart($event, 'sample-node-3')"
    >
      샘플노드3
    </div>
  </aside>
</template>

<script setup lang="ts">
// 드래그 시작 이벤트 핸들러
const onDragStart = (event: DragEvent, nodeType: string) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/vueflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }
}
</script>

<style scoped>
.node-sidebar {
  width: 180px;
  padding: 15px;
  background-color: #f8f8f8;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.node-sidebar h3 {
  margin-top: 0;
  margin-bottom: 5px;
  font-size: 16px;
}

.sidebar-desc {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 12px;
  color: #666;
}

.dnd-node {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 12px;
  text-align: center;
  cursor: grab;
  border-width: 2px;
  border-style: solid;
}

.dnd-node:hover {
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.sample-node-1 {
  background-color: #FFE6CC;
  border-color: #FF9900;
}

.sample-node-2 {
  background-color: #E1D5E7;
  border-color: #9673A6;
}

.sample-node-3 {
  background-color: #DAE8FC;
  border-color: #6C8EBF;
}
</style>
