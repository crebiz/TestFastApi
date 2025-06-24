<template>
  <div>
    <v-card class="budget-card" elevation="3" rounded="lg">
      <v-toolbar flat color="primary" dark class="rounded-t-lg">
        <v-icon class="mr-2 ml-2">mdi-cash-multiple</v-icon>
        <v-toolbar-title class="text-h6 font-weight-medium">예산 관리</v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-6">
        <v-row>
          <!-- 수입 총액 -->
          <v-col cols="12" sm="6" md="4">
            <v-card elevation="2" class="rounded-lg" height="100%">
              <v-card-text class="pa-4">
                <div class="d-flex align-center mb-2">
                  <v-avatar color="success" size="42" class="mr-3">
                    <v-icon color="white">mdi-arrow-down-bold-circle</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-caption text-grey-darken-1 font-weight-medium">수입 총액</div>
                    <div class="text-h4 font-weight-bold text-success">{{ formatCurrency(totalIncome) }}원</div>
                  </div>
                </div>
                <v-divider class="my-3"></v-divider>
                <div class="d-flex align-center">
                  <v-icon color="success" size="small" class="mr-1">mdi-information</v-icon>
                  <span class="text-caption text-grey-darken-1">예산 항목 {{ incomeItemCount }}개</span>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <!-- 지출 총액 -->
          <v-col cols="12" sm="6" md="4">
            <v-card elevation="2" class="rounded-lg" height="100%">
              <v-card-text class="pa-4">
                <div class="d-flex align-center mb-2">
                  <v-avatar color="error" size="42" class="mr-3">
                    <v-icon color="white">mdi-arrow-up-bold-circle</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-caption text-grey-darken-1 font-weight-medium">지출 총액</div>
                    <div class="text-h4 font-weight-bold text-error">{{ formatCurrency(totalExpense) }}원</div>
                  </div>
                </div>
                <v-divider class="my-3"></v-divider>
                <div class="d-flex align-center">
                  <v-icon color="error" size="small" class="mr-1">mdi-information</v-icon>
                  <span class="text-caption text-grey-darken-1">예산 항목 {{ expenseItemCount }}개</span>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <!-- 수지 차액 -->
          <v-col cols="12" sm="6" md="4">
            <v-card elevation="2" class="rounded-lg" height="100%">
              <v-card-text class="pa-4">
                <div class="d-flex align-center mb-2">
                  <v-avatar :color="balanceColor" size="42" class="mr-3">
                    <v-icon color="white">{{ balanceIcon }}</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-caption text-grey-darken-1 font-weight-medium">수지 차액</div>
                    <div class="text-h4 font-weight-bold" :class="balanceTextClass">{{ formatCurrency(balance) }}원</div>
                  </div>
                </div>
                <v-divider class="my-3"></v-divider>
                <div class="d-flex align-center">
                  <v-icon :color="balanceColor" size="small" class="mr-1">mdi-information</v-icon>
                  <span class="text-caption text-grey-darken-1">수입-지출</span>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <!-- 차트 (클릭 시 펼쳐보기) -->
        <v-row class="mt-4">
          <v-col cols="12">
            <v-expansion-panels>
              <v-expansion-panel>
                <v-expansion-panel-title>
                  <div class="d-flex align-center">
                    <v-icon class="mr-2">mdi-chart-bar</v-icon>
                    <span class="text-subtitle-1 font-weight-bold">수지 현황 차트</span>
                  </div>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div class="budget-chart" style="height: 250px; position: relative;">
                    <!-- 차트가 들어갈 자리 -->
                    <div class="text-center text-subtitle-1 text-grey-darken-1" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                      차트 라이브러리 추가 필요
                    </div>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>
      </v-card-text>
      
      <!-- 수입예산 -->
      <v-card-text class="pa-4">
        <div class="d-flex align-center justify-space-between mb-3">
          <div class="d-flex align-center">
            <v-icon color="success" class="mr-2">mdi-arrow-down-bold-circle</v-icon>
            <h2 class="text-h6 font-weight-bold text-success mb-0">수입예산</h2>
          </div>
          <div>
            <v-btn size="small" variant="text" color="success" class="mr-2" @click="expandAllIncome">
              <v-icon size="small" class="mr-1">mdi-unfold-more-horizontal</v-icon>
              전체펼치기
            </v-btn>
            <v-btn size="small" variant="text" color="grey" @click="collapseAllIncome">
              <v-icon size="small" class="mr-1">mdi-unfold-less-horizontal</v-icon>
              모두닫기
            </v-btn>
          </div>
        </div>
        <v-list class="budget-list income-budget" lines="two">
          <BudgetTreeItem 
            v-for="category in incomeCategories" 
            :key="category.id" 
            :node="category" 
            :ref="el => { if (el) incomeRefs.push(el) }" 
          />
        </v-list>
      </v-card-text>
      
      <!-- 지출예산 -->
      <v-card-text class="pa-4 pt-0">
        <div class="d-flex align-center justify-space-between mb-3">
          <div class="d-flex align-center">
            <v-icon color="error" class="mr-2">mdi-arrow-up-bold-circle</v-icon>
            <h2 class="text-h6 font-weight-bold text-error mb-0">지출예산</h2>
          </div>
          <div>
            <v-btn size="small" variant="text" color="error" class="mr-2" @click="expandAllExpense">
              <v-icon size="small" class="mr-1">mdi-unfold-more-horizontal</v-icon>
              전체펼치기
            </v-btn>
            <v-btn size="small" variant="text" color="grey" @click="collapseAllExpense">
              <v-icon size="small" class="mr-1">mdi-unfold-less-horizontal</v-icon>
              모두닫기
            </v-btn>
          </div>
        </div>
        <v-list class="budget-list expense-budget" lines="two">
          <BudgetTreeItem 
            v-for="category in budgetCategories" 
            :key="category.id" 
            :node="category" 
            :ref="el => { if (el) expenseRefs.push(el) }" 
          />
        </v-list>
      </v-card-text>
    </v-card>

    <!-- 예산 항목 편집 다이얼로그 -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editedItem.name" label="항목명"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model.number="editedItem.amount" label="금액" type="number"></v-text-field>
              </v-col>
              <v-col cols="12" v-if="!editedItem.id">
                <v-select v-model="editedItem.categoryId" :items="categoryOptions" label="카테고리" item-title="text" item-value="value"></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="save">저장</v-btn>
          <v-btn @click="close">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import BudgetTreeItem from './BudgetTreeItem.vue';
import { ref, computed, onMounted } from 'vue';

const incomeCategories = ref([
  { id: 'income', name: '소득', icon: 'mdi-cash-multiple', color: '#FFF3D6', iconColor: '#F8C55A', children: [
    { id: 'income_salary', name: '월급', children: [
      { id: 'income_salary_1', name: '정규월급', fund: '668926' },
      { id: 'income_salary_2', name: '프리월급', fund: '668926' },
    ] },
    { id: 'income_tax', name: '세금', children: [
      { id: 'income_tax_1', name: '부가가치세', fund: '668926' }
    ] }
  ] }
]);

const budgetCategories = ref([
  { id: 'tax', name: '부가세', icon: 'mdi-cash-multiple', color: '#FFF3D6', iconColor: '#F8C55A', children: [
    { id: 'tax_vat', name: '부가세', children: [
      { id: 'tax_vat_amount', name: '부가세', fund: '668926' }
    ] }
  ] },
  { id: 'sponsor', name: '후원', icon: 'mdi-hand-heart', color: '#FFE6E6', iconColor: '#FF5757', children: [
    { id: 'sponsor_missionary', name: '선교사후원', children: [
      { id: 'sponsor_missionary_1', name: '김성훈', fund: '30000' },
      { id: 'sponsor_missionary_2', name: '안익상/이난영', fund: '50000' },
      { id: 'sponsor_missionary_3', name: '신웅섭/이미순', fund: '50000' },
      { id: 'sponsor_missionary_4', name: '정천호/정호경', fund: '30000' },
      { id: 'sponsor_missionary_5', name: '오석규/정인애', fund: '30000' },
      { id: 'sponsor_missionary_6', name: '강호석', fund: '10000' }
    ] },
    { id: 'sponsor_organization', name: '단체후원', children: [
      { id: 'sponsor_org_1', name: '부산지방회', fund: '50000' },
      { id: 'sponsor_org_2', name: '남서울지방회', fund: '40000' },
      { id: 'sponsor_org_3', name: '경기남지방회', fund: '40000' },
      { id: 'sponsor_org_4', name: '일상생활사역연구소', fund: '30000' },
      { id: 'sponsor_org_5', name: '굿네이버스', fund: '30000' },
      { id: 'sponsor_org_6', name: '구세군', fund: '30000' }
    ] },
    { id: 'sponsor_offering', name: '헌금', children: [
      { id: 'sponsor_offering_1', name: '감사헌금', fund: '20000' },
      { id: 'sponsor_offering_2', name: '선교헌금', fund: '30000' },
      { id: 'sponsor_offering_3', name: '십일조', fund: '200000' },
      { id: 'sponsor_offering_4', name: '성년부', fund: '50000' }
    ] },
    { id: 'sponsor_savings', name: '후원적립', children: [
      { id: 'sponsor_savings_1', name: '적립', fund: '430000' }
    ] }
  ] },
  { id: 'education', name: '교육', icon: 'mdi-school', color: '#E6F9FF', iconColor: '#57A9FF', children: [
    { id: 'education_investment', name: '교육투자', children: [
      { id: 'education_investment_1', name: '세하연금보험', fund: '150000' },
      { id: 'education_investment_2', name: '세린교육투자', fund: '100000' },
      { id: 'education_investment_3', name: '세하교육투자', fund: '50000' }
    ] },
    { id: 'education_savings', name: '교육적립', children: [
      { id: 'education_savings_1', name: '적립', fund: '1200000' }
    ] }
  ] },
  { id: 'event', name: '경조사', icon: 'mdi-party-popper', color: '#FFF0E6', iconColor: '#FF9F57', children: [
    { id: 'event_parents', name: '부모님', children: [
      { id: 'event_parents_1', name: '부산', fund: '0' }
    ] },
    { id: 'event_fee', name: '회비', children: [
      { id: 'event_fee_1', name: '가족모임회비(광현)', fund: '50000' }
    ] },
    { id: 'event_savings', name: '경조사적립', children: [
      { id: 'event_savings_1', name: '적립', fund: '350000' }
    ] }
  ] },
  { id: 'car', name: '자동차', icon: 'mdi-car', color: '#F0E6FF', iconColor: '#9F57FF', children: [
    { id: 'car_expense', name: '자동차경비', children: [
      { id: 'car_expense_1', name: '경비', fund: '300000' }
    ] },
    { id: 'car_savings', name: '자동차적립', children: [
      { id: 'car_savings_1', name: '적립', fund: '100000' }
    ] }
  ] },
  { id: 'property', name: '부동산', icon: 'mdi-home', color: '#E6F9FF', iconColor: '#57A9FF', children: [
    { id: 'property_management', name: '관리비', children: [
      { id: 'property_management_1', name: '대출이자', fund: '100000' },
      { id: 'property_management_2', name: '관리비', fund: '300000' }
    ] },
    { id: 'property_tax_savings', name: '세금적립', children: [
      { id: 'property_tax_savings_1', name: '적립', fund: '200000' }
    ] }
  ] },
  { id: 'insurance', name: '보험', icon: 'mdi-shield-half', color: '#E6F9FF', iconColor: '#57A9FF', children: [
    { id: 'insurance_national', name: '국가', children: [
      { id: 'insurance_national_1', name: '국민건강보험(광현)', fund: '0' },
      { id: 'insurance_national_2', name: '국민건강보험(혜연)', fund: '68250' },
      { id: 'insurance_national_3', name: '국민연금(광현)', fund: '0' },
      { id: 'insurance_national_4', name: '혜연국민연금', fund: '89550' }
    ] },
    { id: 'insurance_children', name: '어린이', children: [
      { id: 'insurance_children_1', name: '세린어린이보험', fund: '57830' },
      { id: 'insurance_children_2', name: '세하어린이보험', fund: '56260' }
    ] },
    { id: 'insurance_kwang', name: '광현', children: [
      { id: 'insurance_kwang_1', name: '광현종신(신한라이프)', fund: '138600' },
      { id: 'insurance_kwang_2', name: '광현건강(신한라이프)', fund: '134800' },
      { id: 'insurance_kwang_3', name: '광현치아보험', fund: '44152' },
      { id: 'insurance_kwang_4', name: '광현실비보험', fund: '22500' },
      { id: 'insurance_kwang_5', name: '광현건강보험', fund: '130468' }
    ] },
    { id: 'insurance_hye', name: '혜연', children: [
      { id: 'insurance_hye_1', name: '혜연실비보험', fund: '39690' },
      { id: 'insurance_hye_2', name: '혜연정기', fund: '83160' }
    ] }
  ] },
  { id: 'savings', name: '저축', icon: 'mdi-currency-usd', color: '#E6F9FF', iconColor: '#57A9FF', children: [
    { id: 'savings_pension', name: '연금', children: [
      { id: 'savings_pension_1', name: '혜연연금', fund: '0' },
      { id: 'savings_pension_2', name: '광현연금', fund: '300000' },
      { id: 'savings_pension_3', name: '퇴직연금', fund: '200000' }
    ] },
    { id: 'savings_investment', name: '투자', children: [
      { id: 'savings_investment_1', name: '해외펀드', fund: '200000' },
      { id: 'savings_investment_2', name: '펀드', fund: '300000' }
    ] },
    { id: 'savings_subscription', name: '청약', children: [
      { id: 'savings_subscription_1', name: '청약종합저축(광현)', fund: '50000' },
      { id: 'savings_subscription_2', name: '청약종합저축(혜연)', fund: '20000' },
      { id: 'savings_subscription_3', name: '청약종합저축(세린)', fund: '0' },
      { id: 'savings_subscription_4', name: '청약종합저축(세하)', fund: '20000' }
    ] },
    { id: 'savings_extra', name: '여유자금적립', children: [
      { id: 'savings_extra_1', name: '적립', fund: '150000' }
    ] }
  ] },
  { id: 'living', name: '생활비', icon: 'mdi-home', color: '#E6F9FF', iconColor: '#57A9FF', children: [
    { id: 'living_allowance', name: '용돈', children: [
      { id: 'living_allowance_1', name: '혜연용돈', fund: '103230' },
      { id: 'living_allowance_2', name: '광현용돈', fund: '50000' },
      { id: 'living_allowance_3', name: '세린용돈', fund: '50000' },
      { id: 'living_allowance_4', name: '세하용돈', fund: '50000' }
    ] },
    { id: 'living_rest', name: '나머지', children: [
      { id: 'living_rest_1', name: '생활비', fund: '2000000' }
    ] }
  ] }
]);

const dialog = ref(false);
const editedItem = ref<any>({
  id: null,
  name: '',
  amount: 0
});

// 수입 총액 계산
const totalIncome = computed(() => {
  let total = 0;
  
  // 모든 수입 항목의 fund 값을 합산
  const calculateNodeTotal = (node) => {
    if (node.fund) {
      total += parseInt(node.fund, 10) || 0;
    }
    if (node.children) {
      node.children.forEach(child => calculateNodeTotal(child));
    }
  };
  
  incomeCategories.value.forEach(category => calculateNodeTotal(category));
  return total;
});

// 지출 총액 계산
const totalExpense = computed(() => {
  let total = 0;
  
  // 모든 지출 항목의 fund 값을 합산
  const calculateNodeTotal = (node) => {
    if (node.fund) {
      total += parseInt(node.fund, 10) || 0;
    }
    if (node.children) {
      node.children.forEach(child => calculateNodeTotal(child));
    }
  };
  
  budgetCategories.value.forEach(category => calculateNodeTotal(category));
  return total;
});

// 수지 차액 계산
const balance = computed(() => {
  return totalIncome.value - totalExpense.value;
});

// 수지 차액 색상 계산
const balanceColor = computed(() => {
  return balance.value >= 0 ? 'success' : 'error';
});

// 수지 차액 아이콘 계산
const balanceIcon = computed(() => {
  return balance.value >= 0 ? 'mdi-check-circle' : 'mdi-alert-circle';
});

// 수지 차액 텍스트 클래스 계산
const balanceTextClass = computed(() => {
  return balance.value >= 0 ? 'text-success' : 'text-error';
});

// 수입 항목 개수 계산
const incomeItemCount = computed(() => {
  let count = 0;
  
  const countItems = (node) => {
    if (!node.children) {
      count++;
    } else {
      node.children.forEach(child => countItems(child));
    }
  };
  
  incomeCategories.value.forEach(category => countItems(category));
  return count;
});

// 지출 항목 개수 계산
const expenseItemCount = computed(() => {
  let count = 0;
  
  const countItems = (node) => {
    if (!node.children) {
      count++;
    } else {
      node.children.forEach(child => countItems(child));
    }
  };
  
  budgetCategories.value.forEach(category => countItems(category));
  return count;
});

// 금액 포맷팅 함수
const formatCurrency = (value) => {
  return value.toLocaleString('ko-KR');
};

const formTitle = computed(() => editedItem.value.id ? '예산 항목 수정' : '새 예산 항목');

// 다이얼로그 닫기
const close = () => {
  dialog.value = false;
};

// 저장 함수
const save = () => {
  // 저장 로직 구현(실제 로직 필요)
  dialog.value = false;
};

// 펼치기/닫기 기능을 위한 ref 배열
const incomeRefs = ref<any[]>([]);
const expenseRefs = ref<any[]>([]);

// 수입예산 전체 펼치기
const expandAllIncome = async () => {
  try {
    // 수입예산 섹션 선택
    const incomeSection = document.querySelector('.income-budget');
    if (!incomeSection) return;
    
    // 수입예산 섹션 내의 모든 v-list-group 요소를 찾아서 펼치기
    const listGroups = Array.from(incomeSection.querySelectorAll('.v-list-group'));
    
    // 최상위 항목부터 순차적으로 펼치기
    for (const group of listGroups) {
      if (!group.classList.contains('v-list-group--active')) {
        const header = group.querySelector('.v-list-group__header');
        if (header) {
          header.click();
          // 각 클릭 후 약간의 지연을 주어 DOM 업데이트 시간 확보
          await new Promise(resolve => setTimeout(resolve, 50));
        }
      }
    }
    
    // 모든 항목을 한 번 더 처리하여 누락된 항목 확인
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 중간 레벨 항목들 처리
    const middleGroups = Array.from(incomeSection.querySelectorAll('.v-list-group:not(.v-list-group--active)'));
    for (const group of middleGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) {
        header.click();
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
    
    // 마지막 확인
    await new Promise(resolve => setTimeout(resolve, 100));
    const finalGroups = Array.from(incomeSection.querySelectorAll('.v-list-group:not(.v-list-group--active)'));
    for (const group of finalGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) header.click();
    }
  } catch (error) {
    console.error('펼치기 오류:', error);
  }
};

// 수입예산 모두 닫기
const collapseAllIncome = () => {
  try {
    // 수입예산 섹션 선택
    const incomeSection = document.querySelector('.income-budget');
    if (!incomeSection) return;
    
    // 수입예산 섹션 내의 모든 활성화된 v-list-group 요소를 찾아서 닫기
    const listGroups = Array.from(incomeSection.querySelectorAll('.v-list-group.v-list-group--active'));
    
    // 각 항목 닫기
    for (const group of listGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) header.click();
    }
  } catch (error) {
    console.error('닫기 오류:', error);
  }
};

// 지출예산 전체 펼치기
const expandAllExpense = async () => {
  try {
    // 지출예산 섹션 선택
    const expenseSection = document.querySelector('.expense-budget');
    if (!expenseSection) return;
    
    // 지출예산 섹션 내의 모든 v-list-group 요소를 찾아서 펼치기
    const listGroups = Array.from(expenseSection.querySelectorAll('.v-list-group'));
    
    // 최상위 항목부터 순차적으로 펼치기
    for (const group of listGroups) {
      if (!group.classList.contains('v-list-group--active')) {
        const header = group.querySelector('.v-list-group__header');
        if (header) {
          header.click();
          // 각 클릭 후 약간의 지연을 주어 DOM 업데이트 시간 확보
          await new Promise(resolve => setTimeout(resolve, 50));
        }
      }
    }
    
    // 모든 항목을 한 번 더 처리하여 누락된 항목 확인
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 중간 레벨 항목들 처리
    const middleGroups = Array.from(expenseSection.querySelectorAll('.v-list-group:not(.v-list-group--active)'));
    for (const group of middleGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) {
        header.click();
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
    
    // 마지막 확인
    await new Promise(resolve => setTimeout(resolve, 100));
    const finalGroups = Array.from(expenseSection.querySelectorAll('.v-list-group:not(.v-list-group--active)'));
    for (const group of finalGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) header.click();
    }
  } catch (error) {
    console.error('펼치기 오류:', error);
  }
};

// 지출예산 모두 닫기
const collapseAllExpense = () => {
  try {
    // 지출예산 섹션 선택
    const expenseSection = document.querySelector('.expense-budget');
    if (!expenseSection) return;
    
    // 지출예산 섹션 내의 모든 활성화된 v-list-group 요소를 찾아서 닫기
    const listGroups = Array.from(expenseSection.querySelectorAll('.v-list-group.v-list-group--active'));
    
    // 각 항목 닫기
    for (const group of listGroups) {
      const header = group.querySelector('.v-list-group__header');
      if (header) header.click();
    }
  } catch (error) {
    console.error('닫기 오류:', error);
  }
};

// 참조 배열 초기화
onMounted(() => {
  // 참조 배열을 초기화하여 중복 방지
  incomeRefs.value = [];
  expenseRefs.value = [];
});
</script>

<style scoped>
.budget-card {
  margin: 16px 0;
}

.budget-list {
  padding: 8px;
}

.budget-item {
  margin-bottom: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.budget-icon {
  margin-right: 16px;
}
</style>