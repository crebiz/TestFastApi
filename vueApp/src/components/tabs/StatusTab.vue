<template>
  <div class="pa-4">
    <v-row>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-h6 bg-success text-white">
            <v-icon start>mdi-check-circle</v-icon>
            완료된 작업
          </v-card-title>
          <v-card-text>
            <div v-for="task in availableTasks.completed" :key="task" class="mb-2">
              <v-checkbox
                v-model="statusData.completedTasks"
                :value="task"
                :label="task"
                color="success"
                density="compact"
              ></v-checkbox>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-h6 bg-warning text-white">
            <v-icon start>mdi-clock-outline</v-icon>
            진행 중인 작업
          </v-card-title>
          <v-card-text>
            <div v-for="task in availableTasks.inProgress" :key="task" class="mb-2">
              <v-checkbox
                v-model="statusData.inProgressTasks"
                :value="task"
                :label="task"
                color="warning"
                density="compact"
              ></v-checkbox>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-h6 bg-error text-white">
            <v-icon start>mdi-alert-circle</v-icon>
            대기 중인 작업
          </v-card-title>
          <v-card-text>
            <div v-for="task in availableTasks.pending" :key="task" class="mb-2">
              <v-checkbox
                v-model="statusData.pendingTasks"
                :value="task"
                :label="task"
                color="error"
                density="compact"
              ></v-checkbox>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-line</v-icon>
            진행률
          </v-card-title>
          <v-card-text>
            <div class="mb-4">
              <div class="d-flex justify-space-between mb-2">
                <span>전체 진행률</span>
                <span>65%</span>
              </div>
              <v-progress-linear
                v-model="overallProgress"
                color="primary"
                height="8"
                rounded
              ></v-progress-linear>
            </div>
            <div class="mb-4">
              <div class="d-flex justify-space-between mb-2">
                <span>개발 진행률</span>
                <span>80%</span>
              </div>
              <v-progress-linear
                v-model="developmentProgress"
                color="success"
                height="8"
                rounded
              ></v-progress-linear>
            </div>
            <div class="mb-4">
              <div class="d-flex justify-space-between mb-2">
                <span>테스트 진행률</span>
                <span>45%</span>
              </div>
              <v-progress-linear
                v-model="testProgress"
                color="warning"
                height="8"
                rounded
              ></v-progress-linear>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

// === 진행률 관련 반응형 변수들 ===

/** 전체 프로젝트의 진행률을 나타내는 반응형 변수 (0-100%) */
const overallProgress = ref(65);

/** 개발 작업의 진행률을 나타내는 반응형 변수 (0-100%) */
const developmentProgress = ref(80);

/** 테스트 작업의 진행률을 나타내는 반응형 변수 (0-100%) */
const testProgress = ref(45);

/**
 * 각 상태별로 선택 가능한 작업 목록을 정의하는 객체
 * 사용자가 체크박스로 선택할 수 있는 작업들을 카테고리별로 분류
 * 
 * @property {string[]} completed - 완료 가능한 작업 목록
 * @property {string[]} inProgress - 진행 중으로 설정 가능한 작업 목록
 * @property {string[]} pending - 대기 중으로 설정 가능한 작업 목록
 */
const availableTasks = {
  completed: ['프로젝트 설계', 'UI 디자인', '데이터베이스 구축', 'API 설계', '테스트 환경 구축'],
  inProgress: ['API 개발', '테스트 코드 작성', '프론트엔드 개발', '성능 최적화'],
  pending: ['배포 준비', '문서화', '성능 최적화', '사용자 교육', '모니터링 설정']
};

/**
 * 사용자가 선택한 작업들의 상태를 관리하는 반응형 객체
 * 각 배열은 체크박스에서 선택된 작업들을 저장
 * 
 * @property {string[]} completedTasks - 완료된 작업들의 배열
 * @property {string[]} inProgressTasks - 진행 중인 작업들의 배열
 * @property {string[]} pendingTasks - 대기 중인 작업들의 배열
 */
const statusData = reactive({
  completedTasks: ['프로젝트 설계', 'UI 디자인'], // 기본 선택값 (데모용)
  inProgressTasks: ['API 개발'], // 기본 선택값 (데모용)
  pendingTasks: [] // 기본값은 빈 배열
});

/**
 * 현재 상태 관리 데이터를 반환하는 함수
 * 
 * 부모 컴포넌트(TabPage)에서 데이터를 수집할 때 호출됨
 * 임시저장이나 최종 적용 시 현재 선택된 작업 상태들을 가져오기 위해 사용
 * 
 * @returns {object} statusData 객체 (completedTasks, inProgressTasks, pendingTasks 포함)
 */
const getData = () => statusData;

/**
 * 외부에서 전달받은 데이터로 상태 관리 정보를 업데이트하는 함수
 * 
 * 임시저장된 데이터를 불러오거나 초기값을 설정할 때 사용됨
 * 각 배열이 존재하지 않을 경우 빈 배열로 설정하여 안전성 보장
 * 
 * @param {any} data - 설정할 데이터 객체
 * @param {string[]} data.completedTasks - 설정할 완료된 작업 목록
 * @param {string[]} data.inProgressTasks - 설정할 진행 중인 작업 목록
 * @param {string[]} data.pendingTasks - 설정할 대기 중인 작업 목록
 */
const setData = (data: any) => {
  if (data) {
    // 각 배열이 존재하면 해당 값으로, 없으면 빈 배열로 설정
    statusData.completedTasks = data.completedTasks || [];
    statusData.inProgressTasks = data.inProgressTasks || [];
    statusData.pendingTasks = data.pendingTasks || [];
  }
};

/**
 * 상태 관리 데이터를 초기화하는 함수
 * 
 * 모든 작업 선택을 해제하여 빈 배열로 리셋
 * 탭 변경 시 작성중인 데이터를 삭제할 때 사용
 */
const clearData = () => {
  statusData.completedTasks = [];
  statusData.inProgressTasks = [];
  statusData.pendingTasks = [];
};

/**
 * 부모 컴포넌트에서 접근 가능한 메소드들을 노출
 * 
 * TabPage 컴포넌트에서 ref를 통해 이 메소드들을 호출할 수 있게 함
 * - getData: 현재 상태 관리 데이터 조회용
 * - setData: 외부 데이터로 상태 관리 정보 업데이트용
 * - clearData: 상태 관리 데이터 초기화용
 */
defineExpose({
  getData,
  setData,
  clearData
});
</script>
