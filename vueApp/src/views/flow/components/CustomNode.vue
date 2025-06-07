<template>
  <div 
    :class="['custom-node', nodeData.type]"
    @dblclick.stop="onNodeDblClick"
  >
    <!-- 입력 핸들 (위쪽) -->
    <Handle
      type="target"
      position="top"
      :id="`${id}-target-top`"
      class="handle handle-top"
    />
    
    <!-- 입력 핸들 (왼쪽) -->
    <Handle
      type="target"
      position="left"
      :id="`${id}-target-left`"
      class="handle handle-left"
    />
    
    <div class="custom-node-header">
      <div class="custom-node-title">{{ nodeData.label }}</div>
    </div>
    <div class="custom-node-body">
      <div class="custom-node-desc">{{ nodeData.description }}</div>
    </div>
    
    <!-- 출력 핸들 (오른쪽) -->
    <Handle
      type="source"
      position="right"
      :id="`${id}-source-right`"
      class="handle handle-right"
    />
    
    <!-- 출력 핸들 (아래쪽) -->
    <Handle
      type="source"
      position="bottom"
      :id="`${id}-source-bottom`"
      class="handle handle-bottom"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Handle } from '@vue-flow/core'

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  data: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:node', 'dblclick'])

const nodeData = computed(() => props.data)

// 더블클릭 이벤트 처리
const onNodeDblClick = (event: MouseEvent) => {
  // 핸들 클릭 시 이벤트 무시
  const target = event.target as HTMLElement
  if (target.classList.contains('handle')) {
    return
  }
  
  // 부모 컴포넌트로 더블클릭 이벤트 전달
  emit('dblclick', props.id, props.data)
}
</script>

<style scoped>
.custom-node {
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
  text-align: center;
  min-width: 150px;
  background-color: white;
  border-width: 2px;
  border-style: solid;
  position: relative;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}

.custom-node:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}



.handle {
  width: 10px;
  height: 10px;
  background-color: #555;
  border: 2px solid white;
  border-radius: 50%;
}

.handle-top {
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
}

.handle-bottom {
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
}

.handle-left {
  left: -5px;
  top: 50%;
  transform: translateY(-50%);
}

.handle-right {
  right: -5px;
  top: 50%;
  transform: translateY(-50%);
}

.custom-node-header {
  padding-bottom: 6px;
}

.custom-node-title {
  font-weight: bold;
}

.custom-node-body {
  font-size: 10px;
}

.custom-node-desc {
  color: #777;
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
