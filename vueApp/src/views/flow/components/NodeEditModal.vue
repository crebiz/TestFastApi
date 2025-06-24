<template>
  <v-dialog
    :model-value="isOpen"
    max-width="500px"
    @click:outside="close"
    @update:model-value="updateIsOpen"
  >
    <v-card>
      <v-card-title class="text-h6">
        노드 편집
      </v-card-title>
      
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="editedLabel"
            label="노드 이름"
            variant="outlined"
            dense
            autofocus
          ></v-text-field>
          
          <v-textarea
            v-model="editedDescription"
            label="노드 설명"
            variant="outlined"
            rows="3"
            auto-grow
          ></v-textarea>
        </v-form>
      </v-card-text>
      
      <v-card-actions>
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
          variant="text"
          @click="save"
        >
          저장
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

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

// 노드 데이터가 변경될 때 편집 필드 업데이트
watch(() => props.nodeData, (newData) => {
  if (newData) {
    editedLabel.value = newData.label || ''
    editedDescription.value = newData.description || ''
  }
}, { immediate: true })

// 모달 상태 업데이트
const updateIsOpen = (value: boolean) => {
  emit('update:isOpen', value)
}

// 모달 닫기
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
</script>

<style scoped>
.v-card-title {
  border-bottom: 1px solid #eee;
}

.v-form {
  margin-top: 16px;
}
</style>
