<template>
  <div>
    <v-navigation-drawer
      v-model="drawerModel"
      location="right"
      temporary
      width="400"
      class="node-detail-drawer"
    >
    <v-card flat class="h-100">
      <v-toolbar color="primary" dark>
        <v-toolbar-title>노드 상세 정보</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      
      <v-card-text class="pa-4">
        <v-form ref="form">
          <v-text-field
            v-model="editedLabel"
            label="노드 이름"
            variant="outlined"
            class="mb-4"
            dense
          ></v-text-field>
          
          <v-textarea
            v-model="editedDescription"
            label="노드 설명"
            variant="outlined"
            rows="4"
            auto-grow
            class="mb-4"
          ></v-textarea>
          
          <v-divider class="my-4"></v-divider>
          
          <div class="text-subtitle-2 mb-2">노드 타입</div>
          <v-chip
            :color="getNodeTypeColor(nodeData.type)"
            text-color="white"
            class="mb-4"
          >
            {{ getNodeTypeName(nodeData.type) }}
          </v-chip>
          
          <v-divider class="my-4"></v-divider>
          
          <div class="text-subtitle-2 mb-2">노드 ID</div>
          <div class="text-body-2 text-grey-darken-1 mb-4">{{ nodeId }}</div>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="pa-4 pt-0">
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="text"
          @click="close"
        >
          취소
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="save"
        >
          저장
        </v-btn>
      </v-card-actions>
    </v-card>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  nodeId: {
    type: String,
    default: ''
  },
  nodeData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:isOpen', 'save'])

const editedLabel = ref('')
const editedDescription = ref('')

// v-model 처리를 위한 computed 속성
const drawerModel = computed({
  get: () => props.isOpen,
  set: (value) => emit('update:isOpen', value)
})

// 노드 데이터가 변경될 때 편집 필드 업데이트
watch(() => props.nodeData, (newData) => {
  if (newData) {
    editedLabel.value = newData.label || ''
    editedDescription.value = newData.description || ''
  }
}, { immediate: true })

// 드로어 닫기
const close = () => {
  emit('update:isOpen', false)
}

// 변경사항 저장
const save = () => {
  const updatedData = {
    ...props.nodeData,
    label: editedLabel.value,
    description: editedDescription.value
  }
  
  emit('save', props.nodeId, updatedData)
  close()
}

// 노드 타입에 따른 색상 반환
const getNodeTypeColor = (type: string): string => {
  const colorMap: Record<string, string> = {
    'sample-node-1': '#FF9900',
    'sample-node-2': '#9673A6',
    'sample-node-3': '#6C8EBF',
    'data-source': '#05B2DC',
    'preprocessing': '#7AC74F',
    'model': '#FFC857',
    'evaluation': '#E5383B',
    'deployment': '#5E60CE'
  }
  
  return colorMap[type] || '#999999'
}

// 노드 타입에 따른 이름 반환
const getNodeTypeName = (type: string): string => {
  const nameMap: Record<string, string> = {
    'sample-node-1': '샘플노드1',
    'sample-node-2': '샘플노드2',
    'sample-node-3': '샘플노드3',
    'data-source': '데이터 소스',
    'preprocessing': '전처리',
    'model': '모델',
    'evaluation': '평가',
    'deployment': '배포'
  }
  
  return nameMap[type] || '기타'
}
</script>

<style scoped>
.node-detail-drawer {
  z-index: 1000 !important;
  position: fixed !important;
}

.v-card {
  display: flex;
  flex-direction: column;
}

.v-card-text {
  flex-grow: 1;
  overflow-y: auto;
}
</style>
