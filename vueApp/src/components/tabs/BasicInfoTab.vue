<template>
  <div class="pa-4">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="basicInfo.name"
          label="이름"
          variant="outlined"
          density="comfortable"
          class="mb-4"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="basicInfo.email"
          label="이메일"
          variant="outlined"
          density="comfortable"
          class="mb-4"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="basicInfo.phone"
          label="전화번호"
          variant="outlined"
          density="comfortable"
          class="mb-4"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="basicInfo.department"
          label="부서"
          :items="['개발팀', '디자인팀', '기획팀', '마케팅팀']"
          variant="outlined"
          density="comfortable"
          class="mb-4"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea
          v-model="basicInfo.introduction"
          label="자기소개"
          variant="outlined"
          rows="4"
          class="mb-4"
        ></v-textarea>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

/**
 * 기본 정보를 관리하는 반응형 객체
 * 사용자의 개인 정보와 소개를 저장하는 데이터 구조
 * 
 * @property {string} name - 사용자 이름
 * @property {string} email - 사용자 이메일 주소
 * @property {string} phone - 사용자 전화번호
 * @property {string} department - 사용자 소속 부서
 * @property {string} introduction - 사용자 자기소개
 */
const basicInfo = reactive({
  name: '',           // 사용자 이름 (필수 입력 항목)
  email: '',          // 이메일 주소 (연락처 정보)
  phone: '',          // 전화번호 (연락처 정보)
  department: '',     // 소속 부서 (드롭다운에서 선택)
  introduction: ''    // 자기소개 (텍스트 영역에서 입력)
});

/**
 * 현재 기본 정보 데이터를 반환하는 함수
 * 
 * 부모 컴포넌트(TabPage)에서 데이터를 수집할 때 호출됨
 * 임시저장이나 최종 적용 시 현재 입력된 기본 정보를 가져오기 위해 사용
 * 
 * @returns {object} basicInfo 객체 (name, email, phone, department, introduction 포함)
 */
const getData = () => basicInfo;

/**
 * 외부에서 전달받은 데이터로 기본 정보를 업데이트하는 함수
 * 
 * 임시저장된 데이터를 불러오거나 초기값을 설정할 때 사용됨
 * 각 속성이 존재하지 않을 경우 빈 문자열로 설정하여 안전성 보장
 * 
 * @param {any} data - 설정할 데이터 객체
 * @param {string} data.name - 설정할 사용자 이름
 * @param {string} data.email - 설정할 이메일 주소
 * @param {string} data.phone - 설정할 전화번호
 * @param {string} data.department - 설정할 부서명
 * @param {string} data.introduction - 설정할 자기소개
 */
const setData = (data: any) => {
  if (data) {
    // 각 속성이 존재하면 해당 값으로, 없으면 빈 문자열로 설정
    basicInfo.name = data.name || '';
    basicInfo.email = data.email || '';
    basicInfo.phone = data.phone || '';
    basicInfo.department = data.department || '';
    basicInfo.introduction = data.introduction || '';
  }
};

/**
 * 기본 정보 데이터를 초기화하는 함수
 * 
 * 모든 입력 필드를 빈 문자열로 리셋
 * 탭 변경 시 작성중인 데이터를 삭제할 때 사용
 */
const clearData = () => {
  basicInfo.name = '';
  basicInfo.email = '';
  basicInfo.phone = '';
  basicInfo.department = '';
  basicInfo.introduction = '';
};

/**
 * 부모 컴포넌트에서 접근 가능한 메소드들을 노출
 * 
 * TabPage 컴포넌트에서 ref를 통해 이 메소드들을 호출할 수 있게 함
 * - getData: 현재 기본 정보 데이터 조회용
 * - setData: 외부 데이터로 기본 정보 업데이트용
 * - clearData: 기본 정보 데이터 초기화용
 */
defineExpose({
  getData,
  setData,
  clearData
});
</script>
