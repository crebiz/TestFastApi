<template>
  <v-dialog :model-value="modelValue" @update:model-value="updateModelValue" max-width="600px" persistent>
    <v-card>
      <v-card-title class="text-h6 bg-primary text-white">
        <v-icon start>mdi-database-plus</v-icon>
        데이터 입력
      </v-card-title>
      
      <v-card-text class="pa-6">
        <v-form ref="formRef" v-model="isFormValid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.name"
                label="이름"
                variant="outlined"
                density="comfortable"
                :rules="nameRules"
                prepend-inner-icon="mdi-account"
                class="mb-4"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.email"
                label="이메일"
                variant="outlined"
                density="comfortable"
                :rules="emailRules"
                prepend-inner-icon="mdi-email"
                class="mb-4"
              ></v-text-field>
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.phone"
                label="전화번호"
                variant="outlined"
                density="comfortable"
                :rules="phoneRules"
                prepend-inner-icon="mdi-phone"
                class="mb-4"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.department"
                :items="departmentOptions"
                label="부서"
                variant="outlined"
                density="comfortable"
                :rules="departmentRules"
                prepend-inner-icon="mdi-office-building"
                class="mb-4"
              ></v-select>
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.position"
                :items="positionOptions"
                label="직급"
                variant="outlined"
                density="comfortable"
                :rules="positionRules"
                prepend-inner-icon="mdi-account-tie"
                class="mb-4"
              ></v-select>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="formData.salary"
                label="연봉 (만원)"
                variant="outlined"
                density="comfortable"
                type="number"
                :rules="salaryRules"
                prepend-inner-icon="mdi-currency-krw"
                class="mb-4"
              ></v-text-field>
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="formData.introduction"
                label="자기소개"
                variant="outlined"
                rows="4"
                :rules="introductionRules"
                prepend-inner-icon="mdi-text"
                class="mb-4"
              ></v-textarea>
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12" md="6">
              <v-switch
                v-model="formData.isActive"
                label="활성 상태"
                color="primary"
                inset
                class="mb-4"
              ></v-switch>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-switch
                v-model="formData.receiveNotifications"
                label="알림 수신"
                color="success"
                inset
                class="mb-4"
              ></v-switch>
            </v-col>
          </v-row>
        </v-form>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="text-caption text-grey-darken-1">
          <v-icon start size="small">mdi-information</v-icon>
          입력된 데이터는 부모 컴포넌트로 전달됩니다.
        </div>
      </v-card-text>
      
      <v-card-actions class="pa-6 pt-0">
        <v-spacer></v-spacer>
        <v-btn 
          color="secondary" 
          variant="outlined" 
          @click="handleCancel"
          prepend-icon="mdi-close"
        >
          취소
        </v-btn>
        <v-btn 
          color="primary" 
          variant="flat" 
          @click="handleConfirm"
          :disabled="!isFormValid"
          prepend-icon="mdi-check"
        >
          확인
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

/**
 * Props 정의
 */
interface Props {
  modelValue: boolean;
}

defineProps<Props>();

/**
 * Emits 정의
 */
interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm', data: FormData): void;
  (e: 'cancel'): void;
}

const emit = defineEmits<Emits>();

// === 반응형 상태 ===
const formRef = ref();
const isFormValid = ref(false);

/**
 * 폼 데이터 타입 정의
 */
interface FormData {
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

/**
 * 폼 데이터 초기값
 */
const formData = reactive<FormData>({
  name: '김테스트',
  email: 'test@example.com',
  phone: '010-1234-5678',
  department: '개발팀',
  position: '대리',
  salary: 4500,
  introduction: '안녕하세요. 저는 개발팀에서 근무하고 있는 김테스트입니다. 웹 개발과 데이터베이스 관리에 관심이 많으며, 새로운 기술을 배우는 것을 좋아합니다.',
  isActive: true,
  receiveNotifications: true
});

/**
 * 부서 옵션
 */
const departmentOptions = [
  '개발팀',
  '디자인팀',
  '기획팀',
  '마케팅팀',
  '영업팀',
  '인사팀',
  '재무팀',
  '운영팀'
];

/**
 * 직급 옵션
 */
const positionOptions = [
  '인턴',
  '사원',
  '주임',
  '대리',
  '과장',
  '차장',
  '부장',
  '이사',
  '상무',
  '전무'
];

// === 유효성 검사 규칙 ===
const nameRules = [
  (v: string) => !!v || '이름을 입력해주세요.',
  (v: string) => v.length >= 2 || '이름은 2글자 이상이어야 합니다.'
];

const emailRules = [
  (v: string) => !!v || '이메일을 입력해주세요.',
  (v: string) => /.+@.+\..+/.test(v) || '올바른 이메일 형식을 입력해주세요.'
];

const phoneRules = [
  (v: string) => !!v || '전화번호를 입력해주세요.',
  (v: string) => /^01[0-9]-\d{4}-\d{4}$/.test(v) || '올바른 전화번호 형식을 입력해주세요. (예: 010-1234-5678)'
];

const departmentRules = [
  (v: string) => !!v || '부서를 선택해주세요.'
];

const positionRules = [
  (v: string) => !!v || '직급을 선택해주세요.'
];

const salaryRules = [
  (v: number | null) => v !== null || '연봉을 입력해주세요.',
  (v: number | null) => (v !== null && v > 0) || '연봉은 0보다 커야 합니다.'
];

const introductionRules = [
  (v: string) => !!v || '자기소개를 입력해주세요.',
  (v: string) => v.length >= 10 || '자기소개는 10글자 이상이어야 합니다.'
];

// === 메서드 ===
/**
 * 모델 값 업데이트
 */
const updateModelValue = (value: boolean) => {
  emit('update:modelValue', value);
};

/**
 * 확인 버튼 클릭 핸들러
 */
const handleConfirm = async () => {
  const { valid } = await formRef.value.validate();
  
  if (valid) {
    // 폼 데이터 복사본 생성
    const dataToEmit = { ...formData };
    
    console.log('팝업에서 전달할 데이터:', dataToEmit);
    
    // 부모 컴포넌트로 데이터 전달
    emit('confirm', dataToEmit);
    
    // 폼 초기화
    resetForm();
  }
};

/**
 * 취소 버튼 클릭 핸들러
 */
const handleCancel = () => {
  emit('cancel');
  resetForm();
};

/**
 * 폼 초기화
 */
const resetForm = () => {
  Object.assign(formData, {
    name: '김테스트',
    email: 'test@example.com',
    phone: '010-1234-5678',
    department: '개발팀',
    position: '대리',
    salary: 4500,
    introduction: '안녕하세요. 저는 개발팀에서 근무하고 있는 김테스트입니다. 웹 개발과 데이터베이스 관리에 관심이 많으며, 새로운 기술을 배우는 것을 좋아합니다.',
    isActive: true,
    receiveNotifications: true
  });
  
  formRef.value?.resetValidation();
};
</script>

<style scoped>
.v-card-title {
  border-radius: 16px 16px 0 0 !important;
}

.v-text-field, .v-select, .v-textarea {
  margin-bottom: 8px;
}

.v-switch {
  margin-bottom: 0;
}

/* 폼 유효성 검사 스타일 */
.v-input--error .v-field {
  border-color: rgb(var(--v-theme-error)) !important;
}

/* 호버 효과 */
.v-btn:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}
</style>
