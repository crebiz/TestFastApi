<template>
  <v-dialog v-model="isVisible" max-width="600px" persistent>
    <v-card>
      <v-card-title class="text-h6">
        <v-icon start color="primary">mdi-account-circle</v-icon>
        기본정보 미리보기
      </v-card-title>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="previewData.name"
              label="이름"
              variant="outlined"
              density="comfortable"
              readonly
              class="mb-4"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="previewData.email"
              label="이메일"
              variant="outlined"
              density="comfortable"
              readonly
              class="mb-4"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="previewData.phone"
              label="전화번호"
              variant="outlined"
              density="comfortable"
              readonly
              class="mb-4"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="previewData.department"
              label="부서"
              variant="outlined"
              density="comfortable"
              readonly
              class="mb-4"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-textarea
              v-model="previewData.introduction"
              label="자기소개"
              variant="outlined"
              rows="4"
              readonly
              class="mb-4"
            ></v-textarea>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="secondary" variant="outlined" @click="handleCancel">
          <v-icon start>mdi-close</v-icon>
          취소
        </v-btn>
        <v-btn color="primary" variant="flat" @click="handleConfirm">
          <v-icon start>mdi-check</v-icon>
          확인
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';

/**
 * 기본정보 데이터 타입 정의
 */
interface BasicInfoData {
  name: string;
  email: string;
  phone: string;
  department: string;
  introduction: string;
}

/**
 * 컴포넌트 Props 정의
 */
interface Props {
  /** 다이얼로그 표시 여부 */
  modelValue: boolean;
  /** 미리보기할 기본정보 데이터 */
  data?: BasicInfoData;
}

/**
 * 컴포넌트 Emits 정의
 */
interface Emits {
  /** 다이얼로그 표시 상태 변경 이벤트 */
  (e: 'update:modelValue', value: boolean): void;
  /** 확인 버튼 클릭 이벤트 */
  (e: 'confirm', data: BasicInfoData): void;
  /** 취소 버튼 클릭 이벤트 */
  (e: 'cancel'): void;
}

// Props와 Emits 설정
const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  data: () => ({
    name: '김이름',
    email: 'test@naver.com',
    phone: '010-2222-3333',
    department: '개발팀',
    introduction: '소개했음'
  })
});

const emit = defineEmits<Emits>();

/**
 * 다이얼로그 표시 상태를 관리하는 computed 속성
 * v-model을 통해 부모 컴포넌트와 양방향 바인딩
 */
const isVisible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value)
});

/**
 * 미리보기 데이터를 관리하는 반응형 참조
 * props.data의 변경사항을 반영하기 위해 computed 사용
 */
const previewData = computed(() => props.data);

/**
 * 취소 버튼 클릭 핸들러
 * 
 * 다이얼로그를 닫고 부모 컴포넌트에 취소 이벤트를 전달
 */
const handleCancel = () => {
  emit('cancel');
  isVisible.value = false;
};

/**
 * 확인 버튼 클릭 핸들러
 * 
 * 현재 미리보기 데이터를 부모 컴포넌트에 전달하고 다이얼로그를 닫음
 */
const handleConfirm = () => {
  emit('confirm', previewData.value);
  isVisible.value = false;
};
</script>

<style scoped>
/* 필요시 컴포넌트별 스타일 추가 */
</style>
