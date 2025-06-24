<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" rounded="lg" class="mb-4">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="mr-2 ml-2">mdi-tab</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">탭 예제</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>

          <v-tabs :model-value="activeTab" @update:model-value="handleTabChange" color="primary" class="border-b">
            <v-tab value="basic">
              <v-icon start>mdi-account-circle</v-icon>
              기본정보
            </v-tab>
            <v-tab value="status">
              <v-icon start>mdi-chart-line</v-icon>
              상태관리
            </v-tab>
            <v-tab value="ai">
              <v-icon start>mdi-robot</v-icon>
              AI처리
            </v-tab>
          </v-tabs>

          <v-card-text class="pa-4">
            <v-tabs-window v-model="activeTab">
              <v-tabs-window-item value="basic">
                <BasicInfoTab ref="basicInfoRef" />
              </v-tabs-window-item>
              <v-tabs-window-item value="status">
                <StatusTab ref="statusTabRef" />
              </v-tabs-window-item>
              <v-tabs-window-item value="ai">
                <AiTab ref="aiTabRef" />
              </v-tabs-window-item>
            </v-tabs-window>
            
            <!-- 전체 탭 데이터 처리 버튼 -->
            <v-divider class="my-4"></v-divider>
            <v-row class="px-4 pb-4">
              <v-col cols="12" class="d-flex justify-end">
                <v-btn color="info" variant="outlined" class="mr-2" @click="loadTempData">
                  <v-icon start>mdi-download</v-icon>
                  불러오기
                </v-btn>
                <v-btn color="secondary" variant="outlined" class="mr-2" @click="tempSave">
                  <v-icon start>mdi-content-save-outline</v-icon>
                  임시저장
                </v-btn>
                <v-btn color="primary" variant="flat" class="mr-2" @click="applyChanges">
                  <v-icon start>mdi-check</v-icon>
                  적용
                </v-btn>
                <v-btn color="success" variant="outlined" @click="showRouterDialog">
                  <v-icon start>mdi-navigation</v-icon>
                  라우터이동
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 탭 이동 확인 다이얼로그 -->
    <v-dialog v-model="showTabConfirmDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="text-h6">
          <v-icon start color="warning">mdi-alert</v-icon>
          탭 이동 확인
        </v-card-title>
        <v-card-text>
          <p class="mb-3">작성중인 값을 저장하시겠습니까?</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" variant="text" @click="discardAndSwitchTab">
            <v-icon start>mdi-close</v-icon>
            아니오
          </v-btn>
          <v-btn color="primary" variant="flat" @click="saveAndSwitchTab">
            <v-icon start>mdi-content-save</v-icon>
            예
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 메뉴 이동 확인 다이얼로그 -->
    <v-dialog v-model="showMenuConfirmDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="text-h6">
          <v-icon start color="warning">mdi-alert</v-icon>
          메뉴 이동 확인
        </v-card-title>
        <v-card-text>
          <p class="mb-3">작성된 값이 있습니다. 그래도 이동하시겠습니까?</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="outlined" @click="cancelMenuNavigation">
            <v-icon start>mdi-close</v-icon>
            아니오
          </v-btn>
          <v-btn color="primary" variant="flat" @click="proceedMenuNavigation">
            <v-icon start>mdi-check</v-icon>
            예
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 라우터 이동 다이얼로그 -->
    <v-dialog v-model="showRouterConfirmDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title class="text-h6">
          <v-icon start color="info">mdi-navigation</v-icon>
          라우터 이동
        </v-card-title>
        <v-card-text>
          <p class="mb-3">CodePage로 이동하시겠습니까?</p>
          <p class="text-body-2 text-grey-600">
            이것은 라우터 이동 예제입니다. 확인 버튼을 클릭하면 CodePage.vue로 이동합니다.
            현재 작성중인 데이터는 유지됩니다.
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="outlined" @click="cancelRouterNavigation">
            <v-icon start>mdi-close</v-icon>
            취소
          </v-btn>
          <v-btn color="primary" variant="flat" @click="proceedRouterNavigation">
            <v-icon start>mdi-check</v-icon>
            확인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { useRouter } from 'vue-router';
import BasicInfoTab from '@/components/tabs/BasicInfoTab.vue';
import StatusTab from '@/components/tabs/StatusTab.vue';
import AiTab from '@/components/tabs/AiTab.vue';
import { useTabDataStore } from '@/stores/tabData';

// === 반응형 상태 변수들 ===

/** 현재 활성화된 탭을 나타내는 반응형 변수 ('basic', 'status', 'ai' 중 하나) */
const activeTab = ref('basic');

/** BasicInfoTab 컴포넌트의 참조를 저장하는 변수 (getData, setData 메소드 호출용) */
const basicInfoRef = ref();

/** StatusTab 컴포넌트의 참조를 저장하는 변수 (getData, setData 메소드 호출용) */
const statusTabRef = ref();

/** AiTab 컴포넌트의 참조를 저장하는 변수 (getData, setData 메소드 호출용) */
const aiTabRef = ref();

/** 탭 이동 확인 다이얼로그의 표시 여부를 제어하는 반응형 변수 */
const showTabConfirmDialog = ref(false);

/** 메뉴 이동 확인 다이얼로그의 표시 여부를 제어하는 반응형 변수 */
const showMenuConfirmDialog = ref(false);

/** 라우터 이동 확인 다이얼로그의 표시 여부를 제어하는 반응형 변수 */
const showRouterConfirmDialog = ref(false);

/** 탭 변경 시 이동하려는 대상 탭을 임시 저장하는 변수 */
const pendingTab = ref('');

/** 라우트 네비게이션 시 대기 중인 네비게이션 콜백을 저장하는 변수 */
const pendingNavigation = ref<(() => void) | null>(null);

/** 탭 데이터 관리를 위한 Pinia 스토어 인스턴스 */
const tabDataStore = useTabDataStore();

/** Vue Router 인스턴스 */
const router = useRouter();

/**
 * Vue Router의 라우트 떠나기 전 네비게이션 가드
 * 
 * 사용자가 메뉴를 통해 다른 페이지로 이동하려 할 때 호출됨
 * 현재 탭들에 작성된 데이터가 있으면 확인 다이얼로그를 표시하고 네비게이션을 일시 중단
 * 사용자가 선택하면 네비게이션을 계속하거나 취소함
 * 
 * @param {RouteLocationNormalized} to - 이동하려는 라우트 정보
 * @param {RouteLocationNormalized} from - 현재 라우트 정보
 * @param {NavigationGuardNext} next - 네비게이션 제어 함수
 */
onBeforeRouteLeave((to, from, next) => {
  // 현재 탭들에 작성된 데이터가 있는지 확인
  if (hasCurrentTabData()) {
    // 네비게이션을 일시 중단하고 확인 다이얼로그 표시
    pendingNavigation.value = () => next();
    showMenuConfirmDialog.value = true;
    next(false); // 네비게이션 중단
    return;
  } else {
    next();
  }
});

/**
 * 컴포넌트 마운트 시 실행되는 라이프사이클 훅
 * 
 * 디버깅 목적으로 현재 tabDataStore의 상태를 콘솔에 출력
 * 개발 중 데이터 상태를 확인하기 위해 사용
 */
onMounted(() => {
  console.log('=== TabPage 진입 시 tabDataStore 현재 값 ===');
  console.log('임시저장 데이터:', JSON.stringify(tabDataStore.getTempData(), null, 2));
  console.log('임시저장 데이터 존재 여부:', tabDataStore.hasTempData());
  console.log('==========================================');
});

/**
 * 현재 모든 탭의 데이터를 임시저장하는 함수
 * 
 * '임시저장' 버튼 클릭 시 호출됨
 * 각 탭 컴포넌트에서 데이터를 수집하여 하나의 객체로 구성한 후
 * Pinia 스토어에 저장하고 콘솔에 저장된 데이터를 출력
 */
const tempSave = () => {
  // 각 탭의 데이터 수집 (ref를 통해 자식 컴포넌트의 getData 메소드 호출)
  const basicInfoData = basicInfoRef.value?.getData();
  const statusData = statusTabRef.value?.getData();
  const aiData = aiTabRef.value?.getData();

  // 전체 데이터를 TabData 인터페이스 형태로 구성
  const allData = {
    basicInfo: {
      name: basicInfoData?.name || '',
      email: basicInfoData?.email || '',
      phone: basicInfoData?.phone || '',
      department: basicInfoData?.department || '',
      introduction: basicInfoData?.introduction || ''
    },
    status: {
      completedTasks: statusData?.completedTasks || [],
      inProgressTasks: statusData?.inProgressTasks || [],
      pendingTasks: statusData?.pendingTasks || []
    },
    aiSettings: {
      selectedModel: aiData?.selectedModel || '',
      temperature: aiData?.temperature || 0,
      maxTokens: aiData?.maxTokens || 0
    }
  };

  // Pinia store에 임시저장
  tabDataStore.saveTempData(allData);
  
  // 디버깅용 콘솔 출력
  console.log('Pinia Store에 저장된 임시저장 데이터:', JSON.stringify(tabDataStore.getTempData(), null, 2));
};

/**
 * 임시저장된 데이터를 각 탭에 불러오는 함수
 * 
 * '불러오기' 버튼 클릭 시 호출됨
 * Pinia 스토어에서 임시저장된 데이터를 가져와서
 * 각 탭 컴포넌트의 setData 메소드를 통해 데이터를 복원
 */
const loadTempData = () => {
  // Pinia store에서 임시저장된 데이터 불러오기
  const tempData = tabDataStore.getTempData();

  // 각 탭의 데이터를 임시저장된 데이터로 초기화 (ref를 통해 자식 컴포넌트의 setData 메소드 호출)
  basicInfoRef.value?.setData(tempData.basicInfo);
  statusTabRef.value?.setData(tempData.status);
  aiTabRef.value?.setData(tempData.aiSettings);
};

/**
 * 현재 모든 탭의 데이터를 최종 적용하는 함수
 * 
 * '적용' 버튼 클릭 시 호출됨
 * 각 탭에서 데이터를 수집하여 JSON 형태로 콘솔에 출력
 * 실제 서버 전송이나 로컬 저장은 구현되지 않음 (데모용)
 */
const applyChanges = () => {
  // 각 탭의 데이터 수집 (ref를 통해 자식 컴포넌트의 getData 메소드 호출)
  const basicInfoData = basicInfoRef.value?.getData();
  const statusData = statusTabRef.value?.getData();
  const aiData = aiTabRef.value?.getData();

  // 전체 데이터를 TabData 인터페이스 형태로 구성
  const allData = {
    basicInfo: {
      name: basicInfoData?.name || '',
      email: basicInfoData?.email || '',
      phone: basicInfoData?.phone || '',
      department: basicInfoData?.department || '',
      introduction: basicInfoData?.introduction || ''
    },
    status: {
      completedTasks: statusData?.completedTasks || [],
      inProgressTasks: statusData?.inProgressTasks || [],
      pendingTasks: statusData?.pendingTasks || []
    },
    aiSettings: {
      selectedModel: aiData?.selectedModel || '',
      temperature: aiData?.temperature || 0,
      maxTokens: aiData?.maxTokens || 0
    }
  };

  // 최종 적용된 데이터를 JSON 형태로 콘솔 출력 (실제 적용 로직은 여기에 구현)
  console.log('적용된 데이터:', JSON.stringify(allData, null, 2));
};

/**
 * 현재 각 탭에 작성된 데이터가 있는지 확인하는 함수
 * 
 * 각 탭의 현재 데이터를 수집하여 기본값과 다른지 확인
 * 하나라도 기본값과 다르면 true를 반환하여 저장 확인이 필요함을 알림
 * 
 * @returns {boolean} 현재 탭들에 작성된 데이터가 있으면 true, 모두 기본값이면 false
 */
const hasCurrentTabData = () => {
  // 각 탭의 현재 데이터 수집
  const basicInfoData = basicInfoRef.value?.getData();
  const statusData = statusTabRef.value?.getData();
  const aiData = aiTabRef.value?.getData();

  // 기본 정보 탭 데이터 확인
  const hasBasicInfo = basicInfoData && (
    basicInfoData.name !== '' ||
    basicInfoData.email !== '' ||
    basicInfoData.phone !== '' ||
    basicInfoData.department !== '' ||
    basicInfoData.introduction !== ''
  );

  // 상태 관리 탭 데이터 확인
  const hasStatusData = statusData && (
    (statusData.completedTasks && statusData.completedTasks.length > 0) ||
    (statusData.inProgressTasks && statusData.inProgressTasks.length > 0) ||
    (statusData.pendingTasks && statusData.pendingTasks.length > 0)
  );

  // AI 설정 탭 데이터 확인
  const hasAiData = aiData && (
    aiData.selectedModel !== '' ||
    aiData.temperature !== 0 ||
    aiData.maxTokens !== 0
  );

  return hasBasicInfo || hasStatusData || hasAiData;
};

/**
 * 탭 변경을 처리하는 함수
 * 
 * v-tabs 컴포넌트의 @update:modelValue 이벤트 핸들러
 * Vuetify에서 전달하는 unknown 타입을 string으로 안전하게 변환
 * 현재 탭들에 작성된 데이터가 있으면 확인 다이얼로그를 표시하고, 없으면 바로 탭 변경
 * 
 * @param {unknown} newTab - 변경하려는 탭 값 (Vuetify에서 unknown 타입으로 전달)
 */
const handleTabChange = (newTab: unknown) => {
  // unknown 타입을 string으로 안전하게 변환
  const tabValue = String(newTab);
  
  // 현재 탭과 같으면 아무것도 하지 않음
  if (activeTab.value === tabValue) return;
  console.log('tabValue', tabValue);
  console.log('hasCurrentTabData', hasCurrentTabData());
  
  // 현재 탭들에 작성된 데이터가 있는지 확인
  if (hasCurrentTabData()) {
    pendingTab.value = tabValue; // 이동하려는 탭 저장
    showTabConfirmDialog.value = true;
    return; // 탭 변경을 막음
  }
  
  // 작성된 데이터가 없으면 바로 탭 변경
  activeTab.value = tabValue;
};

/**
 * 작성중인 데이터를 삭제하고 탭 변경을 계속하는 함수
 * 
 * 확인 다이얼로그에서 '아니오' 버튼 클릭 시 호출됨
 * 임시저장된 데이터와 각 탭의 작성중인 데이터를 모두 삭제하고 대기 중인 탭으로 이동
 */
const discardAndSwitchTab = () => {
  // 임시저장 데이터 완전 삭제
  tabDataStore.clearTempData();
  
  // 각 탭의 작성중인 데이터도 모두 초기화
  basicInfoRef.value?.clearData();
  statusTabRef.value?.clearData();
  aiTabRef.value?.clearData();
  
  showTabConfirmDialog.value = false;
  
  // 저장된 대기 중인 탭으로 이동
  if (pendingTab.value) {
    activeTab.value = pendingTab.value;
    pendingTab.value = '';
  }
};

/**
 * 현재 데이터를 임시저장하고 탭/네비게이션을 계속하는 함수
 * 
 * 확인 다이얼로그에서 '저장 후 이동' 버튼 클릭 시 호출됨
 * 현재 모든 탭의 데이터를 임시저장한 후 대기 중인 탭 변경이나 네비게이션을 진행
 */
const saveAndSwitchTab = () => {
  // 현재 데이터를 임시저장
  tempSave();
  showTabConfirmDialog.value = false;
  
  // 저장된 대기 중인 탭으로 이동
  if (pendingTab.value) {
    activeTab.value = pendingTab.value;
    pendingTab.value = '';
  }
};

/**
 * 메뉴 이동을 취소하는 함수
 * 
 * 확인 다이얼로그에서 '취소' 버튼 클릭 시 호출됨
 * 다이얼로그를 닫고 모든 대기 중인 작업을 초기화하여 현재 상태를 유지
 */
const cancelMenuNavigation = () => {
  showMenuConfirmDialog.value = false;
  pendingNavigation.value = null; // 대기 중인 네비게이션 초기화
};

/**
 * 메뉴 이동을 계속하는 함수
 * 
 * 확인 다이얼로그에서 '예' 버튼 클릭 시 호출됨
 * 임시저장 데이터를 삭제하고 대기 중인 네비게이션을 계속 진행
 */
const proceedMenuNavigation = () => {
  showMenuConfirmDialog.value = false;
  
  // 임시저장 데이터 삭제
  tabDataStore.clearTempData();
  
  // 대기 중인 네비게이션을 계속 진행
  if (pendingNavigation.value) {
    pendingNavigation.value();
    pendingNavigation.value = null;
  }
};

/**
 * 라우터 이동 확인 다이얼로그를 표시하는 함수
 * 
 * '라우터 이동' 버튼 클릭 시 호출됨
 * 라우터 이동 확인 다이얼로그를 표시
 */
const showRouterDialog = () => {
  showRouterConfirmDialog.value = true;
};

/**
 * 라우터 이동을 취소하는 함수
 * 
 * 확인 다이얼로그에서 '취소' 버튼 클릭 시 호출됨
 * 다이얼로그를 닫고 모든 대기 중인 작업을 초기화하여 현재 상태를 유지
 */
const cancelRouterNavigation = () => {
  showRouterConfirmDialog.value = false;
};

/**
 * 라우터 이동을 계속하는 함수
 * 
 * 확인 다이얼로그에서 '예' 버튼 클릭 시 호출됨
 * 임시저장 데이터를 삭제하고 라우터 이동을 계속 진행
 */
const proceedRouterNavigation = () => {
  showRouterConfirmDialog.value = false;
  
  // 임시저장 데이터 삭제
  tabDataStore.clearTempData();
  
  // CodePage로 라우터 이동
  router.push('/dashboard/code');
};
</script>