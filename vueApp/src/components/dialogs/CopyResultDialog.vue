<template>
  <v-dialog v-model="localShow" max-width="800px" persistent>
    <v-card>
      <v-card-title class="text-h5 pa-6 bg-success text-white">
        <v-icon start>mdi-clipboard-check</v-icon>
        손자 팝업 - 복사 결과
      </v-card-title>
      
      <v-card-text class="pa-6">
        <!-- 결과 요약 -->
        <div class="mb-6">
          <h3 class="text-h6 mb-4">
            <v-icon start color="info">mdi-chart-pie</v-icon>
            처리 결과 요약
          </h3>
          
          <v-row>
            <v-col cols="12" md="4">
              <v-card variant="tonal" color="success" class="pa-4 text-center">
                <v-icon size="48" color="success" class="mb-2">mdi-check-circle</v-icon>
                <div class="text-h4 font-weight-bold">{{ result?.successCount || 0 }}</div>
                <div class="text-body-2">성공</div>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-card variant="tonal" color="error" class="pa-4 text-center">
                <v-icon size="48" color="error" class="mb-2">mdi-alert-circle</v-icon>
                <div class="text-h4 font-weight-bold">{{ result?.failureCount || 0 }}</div>
                <div class="text-body-2">실패</div>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-card variant="tonal" color="info" class="pa-4 text-center">
                <v-icon size="48" color="info" class="mb-2">mdi-format-list-numbered</v-icon>
                <div class="text-h4 font-weight-bold">{{ result?.totalCount || 0 }}</div>
                <div class="text-body-2">전체</div>
              </v-card>
            </v-col>
          </v-row>
        </div>
        
        <!-- 성공률 표시 -->
        <div class="mb-6">
          <v-card variant="outlined" class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-icon color="primary" class="mr-2">mdi-percent</v-icon>
              <span class="text-h6">성공률: {{ successRate }}%</span>
            </div>
            <v-progress-linear
              :model-value="successRate"
              :color="successRate >= 80 ? 'success' : successRate >= 60 ? 'warning' : 'error'"
              height="8"
              rounded
            ></v-progress-linear>
          </v-card>
        </div>
        
        <!-- 실패 목록 -->
        <div v-if="result?.failureList && result.failureList.length > 0" class="mb-4">
          <h3 class="text-h6 mb-4">
            <v-icon start color="error">mdi-alert-circle-outline</v-icon>
            실패 목록 ({{ result.failureCount }}건)
          </h3>
          
          <v-card variant="outlined">
            <v-data-table
              :headers="failureHeaders"
              :items="result.failureList"
              :items-per-page="5"
              class="elevation-0"
            >
              <template v-slot:[`item.id`]="{ item }">
                <v-chip color="error" size="small" variant="tonal">
                  {{ item.id }}
                </v-chip>
              </template>
              
              <template v-slot:[`item.name`]="{ item }">
                <div class="font-weight-medium">{{ item.name }}</div>
              </template>
              
              <template v-slot:[`item.reason`]="{ item }">
                <v-chip 
                  :color="getReasonColor(item.reason)" 
                  size="small" 
                  variant="tonal"
                >
                  {{ item.reason }}
                </v-chip>
              </template>
              
              <template #[`item.errorCode`]="{ item }">
                <code class="text-caption bg-grey-lighten-4 pa-1 rounded">
                  {{ item.errorCode }}
                </code>
              </template>
            </v-data-table>
          </v-card>
        </div>
        
        <!-- 성공 메시지 -->
        <v-alert 
          v-if="result?.failureCount === 0"
          type="success" 
          variant="tonal" 
          class="mb-4"
          icon="mdi-check-all"
        >
          모든 데이터가 성공적으로 복사되었습니다!
        </v-alert>
        
        <!-- 부분 성공 메시지 -->
        <v-alert 
          v-else-if="result && result.successCount > 0"
          type="warning" 
          variant="tonal" 
          class="mb-4"
          icon="mdi-alert"
        >
          일부 데이터 복사에 실패했습니다. 실패한 항목을 확인해주세요.
        </v-alert>
      </v-card-text>
      
      <v-card-actions class="pa-6 pt-0">
        <v-btn
          color="info"
          variant="outlined"
          prepend-icon="mdi-download"
          @click="downloadFailureReport"
          :disabled="!result?.failureList || result.failureList.length === 0"
        >
          실패 리포트 다운로드
        </v-btn>
        
        <v-spacer></v-spacer>
        
        <v-btn
          color="primary"
          variant="flat"
          @click="handleClose"
          prepend-icon="mdi-check"
        >
          확인
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { CopyResult } from './ChildCopyDialog.vue';

// Props 정의
interface Props {
  modelValue: boolean;
  result: CopyResult | null;
}

// Emits 정의
interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'close'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 테이블 헤더 정의
const failureHeaders = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: '데이터명', key: 'name', width: '200px' },
  { title: '실패 사유', key: 'reason', width: '150px' },
  { title: '오류 코드', key: 'errorCode', width: '120px' }
];

// 로컬 표시 상태
const localShow = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// 성공률 계산
const successRate = computed(() => {
  if (!props.result || props.result.totalCount === 0) return 0;
  return Math.round(((props.result.successCount || 0) / props.result.totalCount) * 100);
});

// 실패 사유에 따른 색상 반환
const getReasonColor = (reason: string): string => {
  const colorMap: { [key: string]: string } = {
    '네트워크 연결 오류': 'red',
    '데이터 형식 불일치': 'orange',
    '권한 부족': 'purple',
    '서버 내부 오류': 'red-darken-2',
    '중복 데이터 감지': 'blue'
  };
  
  return colorMap[reason] || 'grey';
};

// 실패 리포트 다운로드
const downloadFailureReport = () => {
  if (!props.result?.failureList || props.result.failureList.length === 0) {
    return;
  }
  
  // CSV 형태로 데이터 생성
  const headers = ['ID', '데이터명', '실패 사유', '오류 코드'];
  const csvContent = [
    headers.join(','),
    ...props.result.failureList.map(item => 
      [item.id, `"${item.name}"`, `"${item.reason}"`, item.errorCode].join(',')
    )
  ].join('\n');
  
  // BOM 추가 (한글 깨짐 방지)
  const bom = '\uFEFF';
  const blob = new Blob([bom + csvContent], { type: 'text/csv;charset=utf-8;' });
  
  // 다운로드 링크 생성
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `복사_실패_리포트_${new Date().toISOString().slice(0, 10)}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  console.log('실패 리포트가 다운로드되었습니다.');
};

// 닫기 처리
const handleClose = () => {
  emit('close');
  localShow.value = false;
};
</script>

<style scoped>
.v-card {
  border-radius: 16px !important;
}

.v-data-table {
  border-radius: 8px;
}

.v-btn:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

code {
  font-family: 'Courier New', monospace;
}

/* 성공률 카드 호버 효과 */
.v-card[variant="tonal"]:hover {
  transform: translateY(-2px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}
</style>
