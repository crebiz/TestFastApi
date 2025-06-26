<template>
  <div class="components-page">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card class="pa-6" elevation="2">
            <v-card-title class="text-h4 mb-4">
              <v-icon start color="primary" size="large">mdi-puzzle</v-icon>
              Components
            </v-card-title>
            
            <v-card-text>
              <!-- 팝업 데이터 전달 예제 섹션 -->
              <v-row class="mb-8">
                <v-col cols="12">
                  <v-card variant="outlined" class="pa-6">
                    <v-card-title class="text-h5 mb-4">
                      <v-icon start color="success">mdi-swap-horizontal</v-icon>
                      팝업 ↔ 부모 데이터 전달 예제
                    </v-card-title>
                    
                    <v-card-text>
                      <p class="text-body-1 mb-4">
                        팝업(자식 컴포넌트)에서 입력한 데이터를 부모 컴포넌트로 전달하는 예제입니다.
                        Vue 3의 emit을 사용하여 데이터를 전달합니다.
                      </p>
                      
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-btn 
                            color="primary" 
                            size="large" 
                            variant="flat"
                            @click="openDataInputDialog"
                            prepend-icon="mdi-plus-circle"
                            block
                          >
                            데이터 입력 팝업 열기
                          </v-btn>
                        </v-col>
                        
                        <v-col cols="12" md="6">
                          <v-btn 
                            color="secondary" 
                            size="large" 
                            variant="outlined"
                            @click="clearReceivedData"
                            prepend-icon="mdi-delete"
                            :disabled="!hasReceivedData"
                            block
                          >
                            받은 데이터 초기화
                          </v-btn>
                        </v-col>
                      </v-row>
                      
                      <!-- 받은 데이터 표시 -->
                      <v-divider class="my-6"></v-divider>
                      
                      <div v-if="hasReceivedData">
                        <h3 class="text-h6 mb-4">
                          <v-icon start color="success">mdi-check-circle</v-icon>
                          팝업에서 받은 데이터
                        </h3>
                        
                        <v-card variant="tonal" color="success" class="pa-4">
                          <v-row>
                            <v-col cols="12" md="6">
                              <v-list class="bg-transparent">
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-account</v-icon>
                                  </template>
                                  <v-list-item-title>이름</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.name }}</v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-email</v-icon>
                                  </template>
                                  <v-list-item-title>이메일</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.email }}</v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-phone</v-icon>
                                  </template>
                                  <v-list-item-title>전화번호</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.phone }}</v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-office-building</v-icon>
                                  </template>
                                  <v-list-item-title>부서</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.department }}</v-list-item-subtitle>
                                </v-list-item>
                              </v-list>
                            </v-col>
                            
                            <v-col cols="12" md="6">
                              <v-list class="bg-transparent">
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-account-tie</v-icon>
                                  </template>
                                  <v-list-item-title>직급</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.position }}</v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-currency-krw</v-icon>
                                  </template>
                                  <v-list-item-title>연봉</v-list-item-title>
                                  <v-list-item-subtitle>{{ receivedData?.salary?.toLocaleString() }}만원</v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-toggle-switch</v-icon>
                                  </template>
                                  <v-list-item-title>활성 상태</v-list-item-title>
                                  <v-list-item-subtitle>
                                    <v-chip :color="receivedData?.isActive ? 'success' : 'error'" size="small">
                                      {{ receivedData?.isActive ? '활성' : '비활성' }}
                                    </v-chip>
                                  </v-list-item-subtitle>
                                </v-list-item>
                                
                                <v-list-item>
                                  <template v-slot:prepend>
                                    <v-icon color="success">mdi-bell</v-icon>
                                  </template>
                                  <v-list-item-title>알림 수신</v-list-item-title>
                                  <v-list-item-subtitle>
                                    <v-chip :color="receivedData?.receiveNotifications ? 'primary' : 'grey'" size="small">
                                      {{ receivedData?.receiveNotifications ? '수신' : '미수신' }}
                                    </v-chip>
                                  </v-list-item-subtitle>
                                </v-list-item>
                              </v-list>
                            </v-col>
                          </v-row>
                          
                          <v-divider class="my-4"></v-divider>
                          
                          <div>
                            <h4 class="text-subtitle-1 mb-2">
                              <v-icon start>mdi-text</v-icon>
                              자기소개
                            </h4>
                            <p class="text-body-2">{{ receivedData?.introduction }}</p>
                          </div>
                        </v-card>
                      </div>
                      
                      <div v-else class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-database-off</v-icon>
                        <p class="text-body-1 text-grey-darken-1">
                          아직 팝업에서 전달받은 데이터가 없습니다.<br>
                          위의 버튼을 클릭하여 데이터를 입력해보세요.
                        </p>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
              
              <div class="text-center py-12">
                <v-icon size="120" color="grey-lighten-1" class="mb-6">
                  mdi-package-variant
                </v-icon>
                
                <h2 class="text-h5 mb-4 text-grey-darken-1">
                  컴포넌트 페이지
                </h2>
                
                <p class="text-body-1 text-grey-darken-1 mb-6 mx-auto" style="max-width: 500px;">
                  이 페이지는 향후 다양한 Vue 컴포넌트들을 관리하고 테스트할 수 있는 공간입니다.
                  현재는 빈 페이지 상태이며, 필요에 따라 컴포넌트 라이브러리나 스토리북과 같은 기능을 추가할 수 있습니다.
                </p>
                
                <v-row justify="center" class="mt-8">
                  <v-col cols="12" sm="6" md="4">
                    <v-card variant="outlined" class="pa-4">
                      <v-icon size="48" color="primary" class="mb-3">mdi-view-grid</v-icon>
                      <h3 class="text-h6 mb-2">컴포넌트 갤러리</h3>
                      <p class="text-body-2 text-grey-darken-1">
                        재사용 가능한 UI 컴포넌트들을 한눈에 볼 수 있는 갤러리
                      </p>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="4">
                    <v-card variant="outlined" class="pa-4">
                      <v-icon size="48" color="success" class="mb-3">mdi-test-tube</v-icon>
                      <h3 class="text-h6 mb-2">컴포넌트 테스트</h3>
                      <p class="text-body-2 text-grey-darken-1">
                        각 컴포넌트의 다양한 상태와 props를 테스트할 수 있는 환경
                      </p>
                    </v-card>
                  </v-col>
                  
                  <v-col cols="12" sm="6" md="4">
                    <v-card variant="outlined" class="pa-4">
                      <v-icon size="48" color="warning" class="mb-3">mdi-book-open-page-variant</v-icon>
                      <h3 class="text-h6 mb-2">문서화</h3>
                      <p class="text-body-2 text-grey-darken-1">
                        컴포넌트 사용법과 API 문서를 확인할 수 있는 공간
                      </p>
                    </v-card>
                  </v-col>
                </v-row>
                
                <v-divider class="my-8"></v-divider>
                
                <div class="text-left">
                  <h3 class="text-h6 mb-4">
                    <v-icon start>mdi-information</v-icon>
                    개발 정보
                  </h3>
                  
                  <v-list class="bg-transparent">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-vuejs</v-icon>
                      </template>
                      <v-list-item-title>Vue 3 Composition API</v-list-item-title>
                      <v-list-item-subtitle>최신 Vue.js 프레임워크 사용</v-list-item-subtitle>
                    </v-list-item>
                    
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="blue">mdi-language-typescript</v-icon>
                      </template>
                      <v-list-item-title>TypeScript 지원</v-list-item-title>
                      <v-list-item-subtitle>타입 안전성과 개발 생산성 향상</v-list-item-subtitle>
                    </v-list-item>
                    
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="purple">mdi-material-design</v-icon>
                      </template>
                      <v-list-item-title>Vuetify 3</v-list-item-title>
                      <v-list-item-subtitle>Material Design 3 기반 UI 컴포넌트</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    
    <!-- 데이터 입력 다이얼로그 -->
    <DataInputDialog
      v-model="showDataInputDialog"
      @confirm="handleDataReceived"
      @cancel="handleDialogCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import DataInputDialog from '@/components/dialogs/DataInputDialog.vue';

/**
 * 받은 데이터 타입 정의
 */
interface ReceivedData {
  name: string;
  email: string;
  phone: string;
  department: string;
  position: string;
  salary: number | null;
  introduction: string;
  isActive: boolean;
  receiveNotifications: boolean;
}

// === 반응형 상태 ===
const showDataInputDialog = ref(false);
const receivedData = ref<ReceivedData | null>(null);

// === 계산된 속성 ===
const hasReceivedData = computed(() => receivedData.value !== null);

// === 메서드 ===
/**
 * 데이터 입력 다이얼로그 열기
 */
const openDataInputDialog = () => {
  showDataInputDialog.value = true;
};

/**
 * 팝업에서 데이터를 받았을 때 처리하는 함수
 * 
 * @param {ReceivedData} data - 팝업에서 전달받은 데이터
 */
const handleDataReceived = (data: ReceivedData) => {
  console.log('부모 컴포넌트에서 받은 데이터:', data);
  
  // 받은 데이터를 상태에 저장
  receivedData.value = { ...data };
  
  // 다이얼로그 닫기
  showDataInputDialog.value = false;
  
  // 성공 메시지 (선택사항)
  console.log('데이터가 성공적으로 전달되었습니다!');
};

/**
 * 다이얼로그 취소 처리
 */
const handleDialogCancel = () => {
  console.log('데이터 입력이 취소되었습니다.');
  showDataInputDialog.value = false;
};

/**
 * 받은 데이터 초기화
 */
const clearReceivedData = () => {
  receivedData.value = null;
  console.log('받은 데이터가 초기화되었습니다.');
};

/**
 * 컴포넌트가 마운트될 때 실행되는 함수
 */
onMounted(() => {
  console.log('Components 페이지가 로드되었습니다.');
});
</script>

<style scoped>
.components-page {
  min-height: 100vh;
}

.v-card {
  border-radius: 16px !important;
}

.v-list-item {
  padding: 8px 0;
}

/* 호버 효과 */
.v-card[variant="outlined"]:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  transform: translateY(-2px);
  transition: all 0.3s ease;
}

/* 아이콘 애니메이션 */
.v-icon {
  transition: transform 0.2s ease;
}

.v-card[variant="outlined"]:hover .v-icon {
  transform: scale(1.1);
}

/* 데이터 표시 카드 스타일 */
.v-card[variant="tonal"] {
  border-radius: 12px !important;
}

/* 버튼 호버 효과 */
.v-btn:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}
</style>
