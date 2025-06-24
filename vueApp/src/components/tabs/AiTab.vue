<template>
  <div class="pa-4">
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-h6">
            <v-icon start>mdi-robot</v-icon>
            AI 모델 설정
          </v-card-title>
          <v-card-text>
            <v-select
              v-model="aiSettings.selectedModel"
              :items="aiModels"
              label="AI 모델 선택"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-select>
            <v-slider
              v-model="aiSettings.temperature"
              label="Temperature"
              min="0"
              max="1"
              step="0.1"
              thumb-label
              class="mb-4"
            ></v-slider>
            <v-slider
              v-model="aiSettings.maxTokens"
              label="Max Tokens"
              min="100"
              max="4000"
              step="100"
              thumb-label
              class="mb-4"
            ></v-slider>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-donut</v-icon>
            처리 통계
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <div class="d-flex justify-space-between">
                <span>오늘 처리된 요청</span>
                <v-chip color="primary" variant="flat">{{ todayRequests }}</v-chip>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-space-between">
                <span>성공률</span>
                <v-chip color="success" variant="flat">{{ successRate }}%</v-chip>
              </div>
            </div>
            <div class="mb-3">
              <div class="d-flex justify-space-between">
                <span>평균 응답시간</span>
                <v-chip color="info" variant="flat">{{ avgResponseTime }}ms</v-chip>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="text-h6">
            <v-icon start>mdi-message-text</v-icon>
            AI 채팅
          </v-card-title>
          <v-card-text>
            <v-textarea
              v-model="userInput"
              label="메시지를 입력하세요"
              variant="outlined"
              rows="3"
              class="mb-4"
            ></v-textarea>
            <div class="d-flex justify-space-between">
              <v-btn color="primary" variant="flat" @click="sendMessage" :loading="isProcessing">
                <v-icon start>mdi-send</v-icon>
                전송
              </v-btn>
              <v-btn color="secondary" variant="outlined" @click="clearChat">
                <v-icon start>mdi-delete</v-icon>
                대화 초기화
              </v-btn>
            </div>
            <v-divider class="my-4"></v-divider>
            <div class="chat-history" style="max-height: 300px; overflow-y: auto;">
              <div v-for="(message, index) in chatHistory" :key="index" class="mb-3">
                <v-chip
                  :color="message.type === 'user' ? 'primary' : 'secondary'"
                  variant="flat"
                  class="mb-2"
                >
                  {{ message.type === 'user' ? '사용자' : 'AI' }}
                </v-chip>
                <div class="ml-2">{{ message.content }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

/**
 * 채팅 메시지의 타입을 정의하는 인터페이스
 * @interface ChatMessage
 * @property {string} type - 메시지 타입 ('user' | 'ai')
 * @property {string} content - 메시지 내용
 */
interface ChatMessage {
  type: 'user' | 'ai';
  content: string;
}

// === 반응형 상태 변수들 ===

/** 사용자가 입력한 메시지를 저장하는 반응형 변수 */
const userInput = ref('');

/** AI 처리 중 상태를 나타내는 로딩 플래그 */
const isProcessing = ref(false);

/** 오늘 처리된 요청 수를 표시하는 통계 데이터 */
const todayRequests = ref(127);

/** AI 처리 성공률을 퍼센트로 표시하는 통계 데이터 */
const successRate = ref(98.5);

/** AI 응답의 평균 시간을 밀리초 단위로 표시하는 통계 데이터 */
const avgResponseTime = ref(850);

/**
 * 사용 가능한 AI 모델 목록
 * 사용자가 선택할 수 있는 AI 모델들의 배열
 */
const aiModels = [
  'GPT-4',
  'GPT-3.5-turbo',
  'Claude-3',
  'Gemini Pro'
];

/**
 * AI 설정을 관리하는 반응형 객체
 * @property {string} selectedModel - 선택된 AI 모델명
 * @property {number} temperature - AI 응답의 창의성 조절 (0-1)
 * @property {number} maxTokens - 최대 토큰 수 제한
 */
const aiSettings = reactive({
  selectedModel: 'GPT-4',    // 기본 선택 모델
  temperature: 0.7,          // 기본 창의성 수준 (0.7은 균형잡힌 값)
  maxTokens: 2000           // 기본 최대 토큰 수
});

/**
 * 채팅 기록을 저장하는 반응형 배열
 * 초기값으로 AI의 환영 메시지를 포함
 */
const chatHistory = ref<ChatMessage[]>([
  { type: 'ai', content: '안녕하세요! AI 어시스턴트입니다. 무엇을 도와드릴까요?' }
]);

// === 메소드 정의 ===

/**
 * 사용자 메시지를 전송하고 AI 응답을 시뮬레이션하는 비동기 함수
 * 
 * 동작 과정:
 * 1. 입력값 유효성 검사 (빈 문자열 체크)
 * 2. 사용자 메시지를 채팅 기록에 추가
 * 3. 로딩 상태 활성화
 * 4. 1.5초 후 AI 응답 시뮬레이션
 * 5. 입력 필드 초기화 및 로딩 상태 해제
 */
const sendMessage = async () => {
  // 입력값이 없거나 공백만 있는 경우 함수 종료
  if (!userInput.value.trim()) return;
  
  // 사용자 메시지를 채팅 기록에 추가
  chatHistory.value.push({
    type: 'user',
    content: userInput.value
  });
  
  // AI 처리 중 상태로 변경 (로딩 스피너 표시)
  isProcessing.value = true;
  
  // 실제 AI API 호출 대신 시뮬레이션된 응답 생성
  // 1.5초 지연 후 응답을 생성하여 실제 AI 처리 시간을 모방
  setTimeout(() => {
    chatHistory.value.push({
      type: 'ai',
      content: `"${userInput.value}"에 대한 AI 응답입니다. 현재는 시뮬레이션 모드입니다.`
    });
    
    // 입력 필드 초기화
    userInput.value = '';
    
    // 로딩 상태 해제
    isProcessing.value = false;
  }, 1500);
};

/**
 * 채팅 기록을 초기화하는 함수
 * 
 * 모든 대화 내용을 삭제하고 초기 환영 메시지로 되돌림
 * 사용자가 새로운 대화를 시작하고 싶을 때 사용
 */
const clearChat = () => {
  chatHistory.value = [
    { type: 'ai', content: '안녕하세요! AI 어시스턴트입니다. 무엇을 도와드릴까요?' }
  ];
};

/**
 * 현재 AI 설정 데이터를 반환하는 함수
 * 
 * 부모 컴포넌트(TabPage)에서 데이터를 수집할 때 호출됨
 * 임시저장이나 최종 적용 시 현재 설정값들을 가져오기 위해 사용
 * 
 * @returns {object} aiSettings 객체 (selectedModel, temperature, maxTokens 포함)
 */
const getData = () => aiSettings;

/**
 * 외부에서 전달받은 데이터로 AI 설정을 업데이트하는 함수
 * 
 * 임시저장된 데이터를 불러오거나 초기값을 설정할 때 사용됨
 * 각 속성이 존재하지 않을 경우 기본값으로 설정하여 안전성 보장
 * 
 * @param {any} data - 설정할 데이터 객체
 * @param {string} data.selectedModel - 설정할 AI 모델명
 * @param {number} data.temperature - 설정할 창의성 수준
 * @param {number} data.maxTokens - 설정할 최대 토큰 수
 */
const setData = (data: any) => {
  if (data) {
    // 각 속성이 존재하면 해당 값으로, 없으면 기본값으로 설정
    aiSettings.selectedModel = data.selectedModel || '';
    aiSettings.temperature = data.temperature || 0;
    aiSettings.maxTokens = data.maxTokens || 0;
  }
};

/**
 * AI 설정 데이터를 초기화하는 함수
 * 
 * 모든 설정을 기본값으로 리셋하고 채팅 기록도 초기화
 * 탭 변경 시 작성중인 데이터를 삭제할 때 사용
 */
const clearData = () => {
  aiSettings.selectedModel = '';
  aiSettings.temperature = 0;
  aiSettings.maxTokens = 0;
  // 채팅 기록도 초기화
  clearChat();
};

/**
 * 부모 컴포넌트에서 접근 가능한 메소드들을 노출
 * 
 * TabPage 컴포넌트에서 ref를 통해 이 메소드들을 호출할 수 있게 함
 * - getData: 현재 설정 데이터 조회용
 * - setData: 외부 데이터로 설정 업데이트용
 * - clearData: AI 설정 데이터 초기화용
 */
defineExpose({
  getData,
  setData,
  clearData
});
</script>
