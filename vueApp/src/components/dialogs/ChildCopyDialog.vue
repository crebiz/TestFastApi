<template>
  <v-dialog v-model="localShow" max-width="600px" persistent>
    <v-card>
      <v-card-title class="text-h5 pa-6 bg-primary text-white">
        <v-icon start>mdi-content-copy</v-icon>
        자녀 팝업 - 복사 기능
      </v-card-title>
      
      <v-card-text class="pa-6">
        <div class="mb-6">
          <h3 class="text-h6 mb-4">
            <v-icon start color="info">mdi-information</v-icon>
            복사할 데이터 목록
          </h3>
          
          <v-card variant="outlined" class="pa-4">
            <v-list>
              <v-list-item v-for="(item, index) in sampleData" :key="index">
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-file-document</v-icon>
                </template>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </div>
        
        <v-alert 
          type="info" 
          variant="tonal" 
          class="mb-4"
          icon="mdi-lightbulb"
        >
          복사 버튼을 클릭하면 API 통합 처리 결과를 확인할 수 있습니다.
        </v-alert>
      </v-card-text>
      
      <v-card-actions class="pa-6 pt-0">
        <v-spacer></v-spacer>
        
        <v-btn
          color="grey"
          variant="outlined"
          @click="handleCancel"
          prepend-icon="mdi-close"
        >
          취소
        </v-btn>
        
        <v-btn
          color="primary"
          variant="flat"
          @click="handleCopy"
          prepend-icon="mdi-content-copy"
          :loading="copying"
        >
          복사 실행
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Props 정의
interface Props {
  modelValue: boolean;
}

// Emits 정의
interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'copy-result', result: CopyResult): void;
  (e: 'cancel'): void;
}

// 복사 결과 타입 정의
export interface CopyResult {
  successCount: number;
  failureCount: number;
  failureList: FailureItem[];
  totalCount: number;
}

export interface FailureItem {
  id: number;
  name: string;
  reason: string;
  errorCode: string;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 반응형 상태
const copying = ref(false);

// 샘플 데이터
const sampleData = ref([
  { name: '사용자 데이터 1', description: '김철수 - 개발팀' },
  { name: '사용자 데이터 2', description: '이영희 - 디자인팀' },
  { name: '사용자 데이터 3', description: '박민수 - 기획팀' },
  { name: '사용자 데이터 4', description: '최지영 - 마케팅팀' },
  { name: '사용자 데이터 5', description: '정우진 - 영업팀' },
  { name: '사용자 데이터 6', description: '한소영 - 인사팀' },
  { name: '사용자 데이터 7', description: '임태호 - 재무팀' },
  { name: '사용자 데이터 8', description: '송미라 - 총무팀' }
]);

// 로컬 표시 상태
const localShow = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// 복사 실행 함수
const handleCopy = async () => {
  copying.value = true;
  
  try {
    // 실제 API 호출을 시뮬레이션 (2초 대기)
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 임의의 결과 생성 (일부 성공, 일부 실패)
    const totalCount = sampleData.value.length;
    const failureCount = Math.floor(Math.random() * 3) + 1; // 1-3개 실패
    const successCount = totalCount - failureCount;
    
    // 실패 목록 생성
    const failureList: FailureItem[] = [];
    const failureIndices = new Set<number>();
    
    // 랜덤하게 실패할 항목들 선택
    while (failureIndices.size < failureCount) {
      failureIndices.add(Math.floor(Math.random() * totalCount));
    }
    
    // 실패 목록 생성
    Array.from(failureIndices).forEach((index, i) => {
      const reasons = [
        '네트워크 연결 오류',
        '데이터 형식 불일치',
        '권한 부족',
        '서버 내부 오류',
        '중복 데이터 감지'
      ];
      
      const errorCodes = ['NET001', 'DATA002', 'AUTH003', 'SRV004', 'DUP005'];
      
      failureList.push({
        id: index + 1,
        name: sampleData.value[index].name,
        reason: reasons[i % reasons.length],
        errorCode: errorCodes[i % errorCodes.length]
      });
    });
    
    const result: CopyResult = {
      successCount,
      failureCount,
      failureList,
      totalCount
    };
    
    // 결과를 부모에게 전달
    emit('copy-result', result);
    
  } catch (error) {
    console.error('복사 처리 중 오류 발생:', error);
  } finally {
    copying.value = false;
  }
};

// 취소 처리
const handleCancel = () => {
  emit('cancel');
  localShow.value = false;
};
</script>

<style scoped>
.v-card {
  border-radius: 16px !important;
}

.v-list-item {
  padding: 8px 0;
}

.v-btn:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}
</style>
