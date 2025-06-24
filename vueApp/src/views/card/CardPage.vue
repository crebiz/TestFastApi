<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" rounded="lg" class="mb-4">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="mr-2 ml-2">mdi-card-bulleted</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">카드사용내역 조회</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>

          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12" md="3">
                <v-select v-model="selectedCardCompany" :items="cardCompanyOptions" label="카드사 선택" variant="outlined"
                  density="comfortable" class="mb-4" hide-details></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select v-model="selectedYear" :items="yearOptions" label="연도" variant="outlined"
                  density="comfortable" class="mb-4" hide-details></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select v-model="selectedMonth" :items="monthOptions" label="월" variant="outlined"
                  density="comfortable" class="mb-4" hide-details></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-btn color="primary" variant="tonal" class="mb-4 mt-2" block @click="fetchCardTransactions">
                  <v-icon start>mdi-magnify</v-icon>
                  조회
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-file-input v-model="excelFile" label="엑셀 파일 업로드" accept=".xlsx, .xls" variant="outlined"
                  density="comfortable" prepend-icon="mdi-file-excel" :disabled="!selectedCardCompany" class="mb-4"
                  @change="handleFileUpload">
                </v-file-input>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn color="primary" variant="elevated" class="mb-4 mt-2" :disabled="!excelFile"
                  @click="processExcelFile" :loading="isLoading" block>
                  <v-icon start>mdi-upload</v-icon>
                  파일 처리
                </v-btn>
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <v-alert v-if="alert && alertType === 'success'" type="success" variant="tonal" closable class="mb-4">
              {{ alertMessage }}
            </v-alert>

            <v-alert v-if="alert && alertType === 'error'" type="error" variant="tonal" closable class="mb-4">
              {{ alertMessage }}
            </v-alert>

            <!-- 버튼은 위에서 구현 -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 통계 정보 표시 카드 영역 -->
    <v-row v-if="cardTransactions.length > 0">
      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="rounded-lg" height="100%">
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-avatar :color="getCardColorSync(selectedCardCompany)" size="42" class="mr-3">
                <v-icon color="var(--text-on-primary)">mdi-currency-krw</v-icon>
              </v-avatar>
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-medium">총 사용금액</div>
                <div class="text-h4 font-weight-bold">{{ formatAmount(totalAmount) }}</div>
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon :color="getCardColorSync(selectedCardCompany)" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">{{ selectedCardCompany || '전체' }} 카드 사용액</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="rounded-lg" height="100%">
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-avatar color="secondary" size="42" class="mr-3">
                <v-icon color="var(--text-on-primary)">mdi-receipt</v-icon>
              </v-avatar>
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-medium">총 사용건수</div>
                <div class="text-h4 font-weight-bold">{{ cardTransactions.length }}</div>
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon color="secondary" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">{{ selectedCardCompany || '전체' }} 카드 거래수</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="rounded-lg" height="100%">
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-avatar color="tertiary" size="42" class="mr-3">
                <v-icon color="var(--text-on-primary)">mdi-store</v-icon>
              </v-avatar>
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-medium">최대 사용금액 가맹점</div>
                <div class="text-subtitle-1 font-weight-bold text-truncate" style="max-width: 150px;">{{
                  topAmountMerchant.name }}</div>
                <div class="text-caption text-success-darken-1">{{ formatAmount(topAmountMerchant.amount) }}</div>
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon color="tertiary" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">최대 지출 가맹점</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card elevation="2" class="rounded-lg" height="100%">
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-2">
              <v-avatar color="secondary" size="42" class="mr-3">
                <v-icon color="var(--text-on-primary)">mdi-store-check</v-icon>
              </v-avatar>
              <div>
                <div class="text-caption text-grey-darken-1 font-weight-medium">최다 방문 가맹점</div>
                <div class="text-subtitle-1 font-weight-bold text-truncate" style="max-width: 150px;">{{
                  topVisitMerchant.name }}</div>
                <div class="text-caption text-warning-darken-1">{{ topVisitMerchant.count }}회 방문</div>
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon color="secondary" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">가장 자주 방문한 가맹점</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 월별 사용금액 그래프 -->
    <v-row v-if="cardTransactions.length > 0">
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="d-flex align-center">
            <v-icon :color="getCardColorSync(selectedCardCompany)" class="mr-2">mdi-chart-line</v-icon>
            월별 사용금액 추이
          </v-card-title>
          <v-card-text>
            <div style="position: relative; height: 200px;">
              <canvas ref="monthlyChart" height="200"></canvas>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 카드 사용내역 테이블 -->
    <v-row>
      <v-col cols="12">
        <v-expansion-panels v-model="tableExpanded">
          <v-expansion-panel>
            <v-expansion-panel-title color="secondary" dark class="rounded-t-lg" style="min-height: 64px; height: 64px;">
              <v-card-item>
                <div class="d-flex align-center w-100">
                  <v-icon class="mr-2">mdi-credit-card</v-icon>
                  <div>
                    <span class="text-h6 font-weight-medium">{{ selectedCardCompany || '카드사' }} 사용내역</span>
                    <span v-if="cardTransactions.length > 0" class="text-subtitle-2 ms-2">(총 {{ cardTransactions.length
                    }}건)</span>
                  </div>
                  <v-spacer></v-spacer>
                  <v-text-field v-model="search" append-icon="mdi-magnify" label="검색" single-line hide-details
                    density="compact" bg-color="rgba(255, 255, 255, 0.05)" class="max-width-200 mr-3"
                    style="max-width: 200px" @click.stop></v-text-field>
                </div>
              </v-card-item>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-card flat>
                <v-card-text class="pa-4">
                  <div class="d-flex align-center mb-3">
                    <v-icon :color="getCardColorSync(selectedCardCompany)" size="small"
                      class="mr-2">mdi-information-outline</v-icon>
                    <span class="text-subtitle-2 font-weight-medium">총 {{ cardTransactions.length }}건의 카드사용내역</span>
                    <v-spacer></v-spacer>
                  </div>

                  <v-divider class="mb-3"></v-divider>

                  <v-data-table name="cardTable" :headers="headers" :items="cardTransactions" :search="search"
                    :loading="isLoading" :items-per-page="-1" hide-default-footer class="rounded-lg" item-key="id" hover
                    :sort-by="sortBy">
                    <template #headers>
                      <tr>
                        <th v-for="header in headers" :key="header.key" class="text-primary font-weight-bold">
                          <div class="d-flex align-center">
                            {{ header.title }}
                            <v-btn v-if="['date', 'cardName', 'merchant', 'amount', 'category'].includes(header.key)"
                              :icon="getSortIcon(header.key)" size="x-small" variant="text"
                              @click="toggleSort(header.key)" class="ml-1">
                            </v-btn>
                          </div>
                        </th>
                      </tr>
                    </template>
                    <template #item="{ item }">
                      <tr>
                        <td @click="openCardDetail(item)" style="cursor: pointer;">{{ formatDate(item.date) }}</td>
                        <td @click="openCardDetail(item)" style="cursor: pointer;">{{ item.cardName }}</td>
                        <td @click="openCardDetail(item)" style="cursor: pointer;">{{ item.merchant }}</td>
                        <td @click="openCardDetail(item)" style="cursor: pointer;" class="text-end">{{
                          formatAmount(item.amount) }}</td>
                        <td @click="openCardDetail(item)" style="cursor: pointer;">{{ item.category }}</td>
                        <td @click="openCardDetail(item)" style="cursor: pointer;">{{ item.note }}</td>
                        <td class="text-center">
                          <v-btn icon size="small" color="error" variant="text" @click.stop="confirmDelete(item)">
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </td>
                      </tr>
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center pa-5">
                        <v-icon size="x-large" color="grey-lighten-1" class="mb-3">mdi-credit-card-off</v-icon>
                        <div class="text-subtitle-1 text-grey">
                          {{ selectedCardCompany ? '조회된 카드 사용내역이 없습니다.' : '카드사를 선택하고 엑셀 파일을 업로드해주세요.' }}
                        </div>
                      </div>
                    </template>
                    <template #bottom>
                      <div class="pa-2 d-flex align-center">
                        <span class="text-caption text-grey-darken-1">
                          * 카드사용내역은 엑셀 파일 업로드 후 조회할 수 있습니다.
                        </span>
                      </div>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>

    <!-- 차트 영역 -->
    <v-row v-if="cardTransactions.length > 0">
      <!-- 분류별 차트 -->
      <v-col cols="12" md="6">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="me-2">mdi-chart-pie</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">분류별 통계</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-4">
            <div class="d-flex justify-center">
              <div style="position: relative; height: 350px; width: 100%;">
                <CategoryChart :chart-data="categoryChartData" />
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon color="primary" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">분류별 거래 금액과 건수 통계</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 카드사별 차트 -->
      <v-col cols="12" md="6">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="me-2">mdi-chart-bar</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">카드사별 통계</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-4">
            <div class="d-flex justify-center">
              <div style="position: relative; height: 350px; width: 100%;">
                <CardCompanyChart :chart-data="cardCompanyChartData" />
              </div>
            </div>
            <v-divider class="my-3"></v-divider>
            <div class="d-flex align-center">
              <v-icon color="primary" size="small" class="mr-1">mdi-information</v-icon>
              <span class="text-caption text-grey-darken-1">카드사별 거래 금액과 건수 통계</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 카드 상세 정보 슬라이드 패널 -->
    <DetailDrawer v-model="cardDetailDrawer" title="카드 사용내역 상세"
      :header-color="selectedCard ? getCardColorSync(selectedCard.cardName) : 'primary'">
      <template v-if="selectedCard">
        <v-sheet rounded class="pa-4 mb-6 bg-grey-lighten-4">
          <!-- 카드 사용내역 기본 정보 표시 -->
          <div class="d-flex align-center mb-2">
            <div>
              <div class="text-h6 font-weight-bold">{{ selectedCard.merchant }}</div>
              <div class="text-caption text-grey">{{ formatDate(selectedCard.date) }} · {{
                formatAmount(selectedCard.amount) }}</div>
            </div>
          </div>
        </v-sheet>

        <v-form @submit.prevent="updateCardTransaction">
          <!-- 분류 선택 -->
          <v-select v-model="selectedCard.category" :items="categoryOptions" label="분류" variant="outlined"
            density="comfortable" class="mb-4" hide-details></v-select>

          <!-- 참고사항 입력 -->
          <v-textarea v-model="selectedCard.note" label="참고사항" variant="outlined" rows="4" auto-grow class="mb-4"
            hide-details></v-textarea>

          <!-- 버튼 영역 -->
          <div class="d-flex justify-space-between mt-6">
            <v-btn color="error" variant="outlined" @click="deleteCardTransaction" :loading="isUpdating">
              <v-icon class="mr-1">mdi-delete</v-icon>
              삭제
            </v-btn>
            <v-btn color="primary" type="submit" :loading="isUpdating">
              <v-icon class="mr-1">mdi-content-save</v-icon>
              저장
            </v-btn>
          </div>
        </v-form>
      </template>
    </DetailDrawer>
  </div>

  <!-- 삭제 확인 다이얼로그 -->
  <v-dialog v-model="deleteDialog" max-width="400">
    <v-card>
      <v-card-title class="text-h6 bg-error text-white pa-4">
        <v-icon class="mr-2">mdi-alert-circle</v-icon>
        삭제 확인
      </v-card-title>
      <v-card-text class="pa-4 pt-6">
        <p>정말로 이 카드 사용내역을 삭제하시겠습니까?</p>
        <div v-if="cardToDelete" class="mt-4 pa-3 bg-grey-lighten-4 rounded">
          <div class="d-flex justify-space-between">
            <span class="text-subtitle-2">이용일자:</span>
            <span>{{ formatDate(cardToDelete.date) }}</span>
          </div>
          <div class="d-flex justify-space-between mt-2">
            <span class="text-subtitle-2">가맹점:</span>
            <span>{{ cardToDelete.merchant }}</span>
          </div>
          <div class="d-flex justify-space-between mt-2">
            <span class="text-subtitle-2">금액:</span>
            <span>{{ formatAmount(cardToDelete.amount) }}</span>
          </div>
        </div>
      </v-card-text>
      <v-card-actions class="pa-4 pt-0">
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="deleteDialog = false">
          취소
        </v-btn>
        <v-btn color="error" variant="elevated" @click="deleteCardFromList" :loading="isLoading">
          삭제
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import axios from 'axios';
import CategoryChart from '@/components/chart/CategoryChart.vue';
import CardCompanyChart from '@/components/chart/CardCompanyChart.vue';
import DetailDrawer from '@/components/common/DetailDrawer.vue';
import { getApiUrl } from '@/config/api';
import { getCardColorSync, formatAmount, formatDate, getCardCompanyCodes, CodeDetail } from '@/utils/common';
import Chart from 'chart.js/auto';

// 타입 정의
interface CardTransaction {
  id: string;
  date: string;
  cardName: string;
  merchant: string;
  amount: number;
  category: string;
  note: string;
}

interface CardApiResponse {
  id: string;
  transaction_date: string;
  card_code: string;
  merchant: string;
  amount: number;
  category: string | null;
  note: string | null;
  created_at: string;
  updated_at: string;
}

// 카드사 선택
const selectedCardCompany = ref('전체'); // 기본값을 '전체'로 설정

// 연도 옵션 추가
const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const yearOptions = ref([currentYear, currentYear - 1, currentYear - 2]);
const selectedYear = ref(currentYear);

// 월 옵션 추가
const monthOptions = ref([
  { title: '1월', value: 1 },
  { title: '2월', value: 2 },
  { title: '3월', value: 3 },
  { title: '4월', value: 4 },
  { title: '5월', value: 5 },
  { title: '6월', value: 6 },
  { title: '7월', value: 7 },
  { title: '8월', value: 8 },
  { title: '9월', value: 9 },
  { title: '10월', value: 10 },
  { title: '11월', value: 11 },
  { title: '12월', value: 12 },
]);
// 현재 월에서 1달 전을 기본값으로 설정
const prevMonth = currentDate.getMonth(); // 0-based (0: 1월, 11: 12월)
const selectedMonth = ref(prevMonth === 0 ? 12 : prevMonth); // 1월이면 12월로 설정
const excelFile = ref<File | null>(null);
const isLoading = ref(false);
const alert = ref(false);
const alertType = ref('success');
const alertMessage = ref('');
const search = ref(''); // 검색어 변수 추가
type SortOrder = 'asc' | 'desc';
const sortBy = ref<Array<{ key: string, order: SortOrder }>>([{ key: 'date', order: 'desc' }]);

// 카드 상세 정보 관련 변수
const cardDetailDrawer = ref(false);
const selectedCard = ref<CardTransaction | null>(null);
const categoryOptions = ref<{ value: string, title: string }[]>([]);
const isUpdating = ref(false);

// 카드 사용내역 목록
const cardTransactions = ref<CardTransaction[]>([]);

// 테이블 확장/축소 상태
const tableExpanded = ref([0]); // 기본적으로 확장된 상태

// 통계 데이터
const totalAmount = ref(0);
const topAmountMerchant = ref({ name: '-', amount: 0 });
const topVisitMerchant = ref({ name: '-', count: 0 });
const categoryStats = ref<Record<string, { amount: number, count: number }>>({});
const cardCompanyStats = ref<Record<string, { amount: number, count: number }>>({});
const monthlyStats = ref<Array<{ month: string, amount: number, count: number }>>([]);

// 차트 관련 변수
const monthlyChart = ref<HTMLCanvasElement | null>(null);
let monthlyChartInstance: Chart | null = null;

// 월별 차트 초기화 함수
const initMonthlyChart = () => {
  // 이미 차트가 있는 경우 제거
  if (monthlyChartInstance) {
    monthlyChartInstance.destroy();
    monthlyChartInstance = null;
  }

  // 차트 요소가 없는 경우 종료
  if (!monthlyChart.value) {
    console.error('차트 요소를 찾을 수 없습니다.');
    return;
  }

  // 월별 데이터가 없는 경우 종료
  if (monthlyStats.value.length === 0) {
    console.warn('표시할 월별 데이터가 없습니다.');
    return;
  }

  // 차트 데이터 구성 - 전월까지만 표시
  // 현재 월을 제외하고 전월까지만 표시하기 위해 마지막 월 제외
  const filteredMonthlyStats = [...monthlyStats.value];
  if (filteredMonthlyStats.length > 0) {
    // 마지막 월(현재 월) 제외
    filteredMonthlyStats.pop();
  }

  const labels = filteredMonthlyStats.map(stat => {
    // YYYY-MM 형식에서 월 표시를 더 보기 좋게 변환
    const [year, month] = stat.month.split('-');
    return `${year}년 ${parseInt(month)}월`;
  });
  const amounts = filteredMonthlyStats.map(stat => stat.amount);

  // 카드사 색상 가져오기
  const chartColor = getCardColorSync(selectedCardCompany.value);
  let lineColor = '#1976D2'; // 기본 파란색

  // Vuetify 색상 코드를 RGB 형식으로 변환
  if (chartColor === 'primary') {
    lineColor = '#1976D2';
  } else if (chartColor === 'error' || chartColor === 'red-darken-1') {
    lineColor = 'var(--color-error)';
  } else if (chartColor === 'blue-darken-1') {
    lineColor = 'var(--color-blue)';
  } else if (chartColor === 'green-darken-1') {
    lineColor = 'var(--color-green)';
  } else if (chartColor === 'orange-darken-1') {
    lineColor = 'var(--color-orange)';
  } else if (chartColor === 'purple-darken-1') {
    lineColor = 'var(--color-purple)';
  }

  // 차트 생성
  monthlyChartInstance = new Chart(monthlyChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '월별 사용금액',
        data: amounts,
        borderColor: lineColor,
        backgroundColor: lineColor + '20', // 20% 투명도
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointBackgroundColor: lineColor,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return formatAmount(Number(value));
            }
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return formatAmount(context.parsed.y);
            }
          }
        }
      }
    }
  });

  console.log('월별 차트 초기화 완료');
};

// 전체 데이터의 월별 통계 데이터 가져오기
const fetchAllMonthlyStats = async () => {
  try {
    // 월별 통계 전용 API 요청
    const url = getApiUrl('/cards/all-monthly-stats');
    console.log('전체 월별 통계 API 요청 URL:', url);

    const response = await axios.get(url);
    const monthlyStatsData = response.data;

    // 월별 통계 데이터 처리
    monthlyStats.value = monthlyStatsData;

    // 월별 차트 초기화
    await nextTick();
    initMonthlyChart();

    console.log('전체 월별 통계 데이터 받음:', monthlyStatsData);
  } catch (error) {
    console.error('월별 통계 데이터 조회 오류:', error);
    // 오류 발생 시 빈 배열로 초기화
    monthlyStats.value = [];
  }
};

// 카드사 코드 목록 (공통 코드에서 가져옴)
const cardCompanyCodes = ref<CodeDetail[]>([]);

// 카드사 코드 가져오기
const fetchCardCompanyCodes = async () => {
  try {
    cardCompanyCodes.value = await getCardCompanyCodes();
    console.log('카드사 코드 목록 가져오기 성공:', cardCompanyCodes.value);
  } catch (error) {
    console.error('카드사 코드 목록 가져오기 오류:', error);
  }
};

// 카드사별 색상과 아이콘은 common.ts의 getCardColor 함수를 통해 관리합니다.

// 카드사 선택 옵션 (CodeDetail 배열에서 카드사명만 추출)
const cardCompanyOptions = computed(() => {
  return cardCompanyCodes.value.map(code => code.name);
});

// 카드 코드로 카드명을 조회하는 함수 (코드 테이블 기반)
const getCardNameFromCodes = (cardCode: string): string => {
  const foundCard = cardCompanyCodes.value.find(code => code.id === cardCode);
  return foundCard ? foundCard.name : '기타 카드';
};

// 테이블 헤더 정의
const headers = [
  { title: '이용일자', key: 'date', align: 'start' as const, sortable: true },
  { title: '이용카드', key: 'cardName', align: 'start' as const, sortable: true },
  { title: '가맹점', key: 'merchant', align: 'start' as const, sortable: true },
  { title: '사용금액', key: 'amount', align: 'end' as const, sortable: true },
  { title: '분류', key: 'category', align: 'start' as const, sortable: true },
  { title: '참고사항', key: 'note', align: 'start' as const, sortable: true },
  { title: '작업', key: 'actions', align: 'center' as const, sortable: false },
];

// 분류별 차트 데이터
const categoryChartData = computed(() => {
  const categories = Object.keys(categoryStats.value);
  const amountData = categories.map(category => categoryStats.value[category].amount);
  const countData = categories.map(category => categoryStats.value[category].count);

  return {
    labels: categories,
    datasets: [
      {
        label: '금액(만원)',
        backgroundColor: 'var(--color-background)',
        borderColor: 'var(--color-primary)',
        borderWidth: 1,
        data: amountData.map(amount => Math.round(amount / 10000)), // 만원 단위로 변환
        yAxisID: 'y'
      },
      {
        label: '건수',
        backgroundColor: 'var(--color-background)',
        borderColor: 'var(--color-error)',
        borderWidth: 1,
        data: countData,
        yAxisID: 'y1'
      }
    ]
  };
});

// 카드사별 차트 데이터
const cardCompanyChartData = computed(() => {
  const companies = Object.keys(cardCompanyStats.value);
  const amountData = companies.map(company => cardCompanyStats.value[company].amount);
  const countData = companies.map(company => cardCompanyStats.value[company].count);

  return {
    labels: companies,
    datasets: [
      {
        label: '금액(만원)',
        backgroundColor: 'var(--color-background)',
        borderColor: 'var(--color-blue)',
        borderWidth: 1,
        data: amountData.map(amount => Math.round(amount / 10000)), // 만원 단위로 변환
        yAxisID: 'y'
      },
      {
        label: '건수',
        backgroundColor: 'var(--color-background)',
        borderColor: 'var(--color-purple)',
        borderWidth: 1,
        data: countData,
        yAxisID: 'y1'
      }
    ]
  };
});

// 정렬 아이콘 가져오기
const getSortIcon = (key: string) => {
  const currentSort = sortBy.value[0];
  if (currentSort.key !== key) return 'mdi-sort';
  return currentSort.order === 'asc' ? 'mdi-sort-ascending' : 'mdi-sort-descending';
};

// 정렬 토글 함수
const toggleSort = (key: string) => {
  const currentSort = sortBy.value[0];
  if (currentSort.key === key) {
    // 같은 컬럼이면 정렬 방향만 변경
    const newOrder: SortOrder = currentSort.order === 'asc' ? 'desc' : 'asc';
    sortBy.value = [{ key, order: newOrder }];
  } else {
    // 다른 컬럼이면 해당 컬럼으로 정렬 (기본 내림차순)
    sortBy.value = [{ key, order: 'desc' }];
  }
};

// 카드 상세 정보 열기
const openCardDetail = (card: CardTransaction) => {
  selectedCard.value = { ...card };
  cardDetailDrawer.value = true;
  // 분류 코드 목록 가져오기
  fetchCategoryOptions();
};

// 분류 코드 목록 가져오기
const fetchCategoryOptions = async () => {
  try {
    const response = await axios.get(getApiUrl('/api/codes/details'), {
      params: { group_id: 'CARD_CATEGORY_KEYWORD' }
    });
    categoryOptions.value = response.data.map((item: any) => ({
      value: item.name,
      title: item.name
    }));
  } catch (error) {
    console.error('분류 코드 목록 조회 실패:', error);
    alertMessage.value = '분류 코드 목록을 가져오는데 실패했습니다.';
    alertType.value = 'error';
    alert.value = true;
  }
};

// 카드 사용내역 수정
const updateCardTransaction = async () => {
  if (!selectedCard.value) return;

  isUpdating.value = true;
  try {
    await axios.put(getApiUrl('/cards/') + selectedCard.value.id, {
      category: selectedCard.value.category,
      note: selectedCard.value.note
    });

    // 성공 메시지 표시
    alertMessage.value = '카드 사용내역이 수정되었습니다.';
    alertType.value = 'success';
    alert.value = true;

    // 목록 갱신
    await fetchCardTransactions();

    // 상세 패널 닫기
    cardDetailDrawer.value = false;
  } catch (error) {
    console.error('카드 사용내역 수정 실패:', error);
    alertMessage.value = '카드 사용내역 수정에 실패했습니다.';
    alertType.value = 'error';
    alert.value = true;
  } finally {
    isUpdating.value = false;
  }
};

// 삭제 확인 다이얼로그
const deleteDialog = ref(false);
const cardToDelete = ref<CardTransaction | null>(null);

// 삭제 확인 팝업 표시
const confirmDelete = (card: CardTransaction) => {
  cardToDelete.value = card;
  deleteDialog.value = true;
};

// 카드 사용내역 삭제 (상세 패널에서)
const deleteCardTransaction = async () => {
  if (!selectedCard.value) return;

  isUpdating.value = true;
  try {
    await axios.delete(getApiUrl('/cards/') + selectedCard.value.id);

    // 성공 메시지 표시
    alertMessage.value = '카드 사용내역이 삭제되었습니다.';
    alertType.value = 'success';
    alert.value = true;

    // 목록 갱신
    await fetchCardTransactions();

    // 상세 패널 닫기
    cardDetailDrawer.value = false;
  } catch (error) {
    console.error('카드 사용내역 삭제 실패:', error);
    alertMessage.value = '카드 사용내역 삭제에 실패했습니다.';
    alertType.value = 'error';
    alert.value = true;
  } finally {
    isUpdating.value = false;
  }
};

// 카드 사용내역 삭제 (목록에서)
const deleteCardFromList = async () => {
  if (!cardToDelete.value) return;

  isLoading.value = true;
  try {
    await axios.delete(getApiUrl('/cards/') + cardToDelete.value.id);

    // 성공 메시지 표시
    alertMessage.value = '카드 사용내역이 삭제되었습니다.';
    alertType.value = 'success';
    alert.value = true;

    // 목록 갱신
    await fetchCardTransactions();

    // 다이얼로그 닫기
    deleteDialog.value = false;
    cardToDelete.value = null;
  } catch (error) {
    console.error('카드 사용내역 삭제 실패:', error);
    alertMessage.value = '카드 사용내역 삭제에 실패했습니다.';
    alertType.value = 'error';
    alert.value = true;
  } finally {
    isLoading.value = false;
  }
};

// 파일 업로드 처리
const handleFileUpload = (file: File | null) => {
  if (file) {
    alert.value = false;
  }
};

// 엑셀 파일 처리 - 백엔드 API를 호출하여 엑셀 파일 업로드 및 처리
const processExcelFile = async () => {
  if (!excelFile.value) {
    alertMessage.value = '파일을 선택해주세요.';
    alertType.value = 'error';
    alert.value = true;
    return;
  }

  isLoading.value = true;
  alert.value = false;

  try {
    // FormData 생성
    const formData = new FormData();
    formData.append('file', excelFile.value);
    formData.append('year', selectedYear.value.toString());
    formData.append('month', selectedMonth.value.toString());

    // API 호출
    const response = await axios.post(getApiUrl('/cards/upload'), formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // 성공 처리
    alertMessage.value = `${selectedCardCompany.value} 엑셀 파일이 성공적으로 처리되었습니다. (총 ${response.data.result.success_count}건 처리)`;
    alertType.value = 'success';
    alert.value = true;

    // 업로드 후 카드 사용내역 목록 조회
    fetchCardTransactions();

    // 파일 초기화
    excelFile.value = null;
  } catch (error) {
    console.error('엑셀 파일 업로드 오류:', error);
    alertMessage.value = '파일 처리 중 오류가 발생했습니다.';
    alertType.value = 'error';
    alert.value = true;
  } finally {
    isLoading.value = false;
  }
};

// 날짜, 금액, 카드 관련 함수는 common.ts에서 가져옵니다.
// formatDate, formatAmount, getCardColor, getCardIcon 함수 사용

// 통계 데이터 계산 함수 - 백엔드 API 사용
const calculateStatistics = async () => {
  try {
    // 필터링 파라미터 구성
    const params: Record<string, string | number> = {};

    // 카드사 코드 필터링 (선택된 경우)
    if (selectedCardCompany.value && selectedCardCompany.value !== '전체') {
      const selectedCard = cardCompanyCodes.value.find(code => code.name === selectedCardCompany.value);
      if (selectedCard) {
        params.card_code = selectedCard.id;
      }
    }

    // 연도, 월 필터링
    if (selectedYear.value) {
      params.year = selectedYear.value;
    }

    if (selectedMonth.value) {
      params.month = selectedMonth.value;
    }

    // 통계 API 요청
    const url = getApiUrl('/cards/statistics');
    console.log('통계 API 요청 URL:', url, '파라미터:', params);

    const response = await axios.get(url, { params });
    const statistics = response.data;

    // 통계 데이터 업데이트
    totalAmount.value = statistics.total_amount;
    topAmountMerchant.value = {
      name: statistics.top_amount_merchant.name,
      amount: statistics.top_amount_merchant.amount
    };
    topVisitMerchant.value = {
      name: statistics.top_visit_merchant.name,
      count: statistics.top_visit_merchant.count
    };

    // 카테고리별 통계 변환
    const categoryStatsObj: Record<string, { amount: number, count: number }> = {};
    statistics.category_stats.forEach((stat: { name: string, amount: number, count: number }) => {
      categoryStatsObj[stat.name] = {
        amount: stat.amount,
        count: stat.count
      };
    });
    categoryStats.value = categoryStatsObj;

    // 카드사별 통계 변환
    const cardCompanyStatsObj: Record<string, { amount: number, count: number }> = {};
    statistics.card_company_stats.forEach((stat: { name: string, amount: number, count: number }) => {
      // 카드사 코드를 카드사명으로 변환
      const cardName = getCardNameFromCodes(stat.name);
      cardCompanyStatsObj[cardName] = {
        amount: stat.amount,
        count: stat.count
      };
    });
    cardCompanyStats.value = cardCompanyStatsObj;

    console.log('백엔드 통계 데이터 받음:', statistics);
  } catch (error) {
    console.error('통계 데이터 조회 오류:', error);

    // 오류 발생 시 기본값으로 초기화
    totalAmount.value = 0;
    topAmountMerchant.value = { name: '-', amount: 0 };
    topVisitMerchant.value = { name: '-', count: 0 };
    categoryStats.value = {};
    cardCompanyStats.value = {};
  }
}

// 카드 사용내역 목록 조회
const fetchCardTransactions = async () => {
  try {
    isLoading.value = true;
    console.log('카드 사용내역 조회 시작...', selectedCardCompany.value, selectedYear.value, selectedMonth.value);

    // 조회 파라미터 구성
    const params: Record<string, string | number> = {};

    // 카드사 코드 필터링 (선택된 경우)
    if (selectedCardCompany.value && selectedCardCompany.value !== '전체') {
      const selectedCard = cardCompanyCodes.value.find(code => code.name === selectedCardCompany.value);
      if (selectedCard) {
        params.card_code = selectedCard.id;
      }
    }

    // 연도, 월 필터링
    if (selectedYear.value) {
      params.year = selectedYear.value;
    }

    if (selectedMonth.value) {
      params.month = selectedMonth.value;
    }

    // API 요청
    const url = getApiUrl('/cards/');
    console.log('API 요청 URL:', url, '파라미터:', params);

    // '전체' 선택 시에는 필터링 없이 모든 카드사 데이터 조회

    const response = await axios.get(url, { params });

    // 데이터 변환 및 정렬 (백엔드 응답 형식에 맞게 변환)
    const transactions = response.data.map((card: CardApiResponse): CardTransaction => ({
      id: card.id,
      date: card.transaction_date.substring(0, 4) + '-' +
        card.transaction_date.substring(4, 6) + '-' +
        card.transaction_date.substring(6, 8),
      cardName: getCardNameFromCodes(card.card_code),
      merchant: card.merchant,
      amount: card.amount,
      category: card.category || '기타',
      note: card.note || ''
    }));

    // 이용일자, 분류, 사용금액, 가맹점 순으로 정렬
    cardTransactions.value = transactions.sort((a: CardTransaction, b: CardTransaction) => {
      // 1. 이용일자 (내림차순)
      const dateComparison = b.date.localeCompare(a.date);
      if (dateComparison !== 0) return dateComparison;

      // 2. 분류
      const categoryComparison = a.category.localeCompare(b.category);
      if (categoryComparison !== 0) return categoryComparison;

      // 3. 사용금액 (내림차순)
      const amountComparison = b.amount - a.amount;
      if (amountComparison !== 0) return amountComparison;

      // 4. 가맹점
      return a.merchant.localeCompare(b.merchant);
    });

    // 통계 데이터 계산
    await calculateStatistics();

    // 월별 통계 데이터도 함께 갱신
    await fetchAllMonthlyStats();
  } catch (error: any) {
    console.error('카드 사용내역 조회 오류:', error);
    // 오류 상세 정보 추가 로깅
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    } else if (error.request) {
      console.error('Request error:', error.request);
    } else {
      console.error('Error message:', error.message);
    }

    alertMessage.value = '카드 사용내역 조회 중 오류가 발생했습니다.';
    alertType.value = 'error';
    alert.value = true;

    // 오류 발생 시 빈 배열로 초기화
    cardTransactions.value = [];
  } finally {
    isLoading.value = false;
    console.log('카드 사용내역 조회 완료');
  }
};

// 공통 유틸리티에서 카드 관련 함수 가져오기
// getCardNameSync 함수는 common.ts에서 가져오는 동기식 함수입니다.
// 비동기 getCardName 대신 사용하여 데이터 변환 과정에서 즉시 카드명을 얻을 수 있습니다.

// 컴포넌트 마운트 시 카드사 코드 및 카드 사용내역 조회
onMounted(async () => {
  console.log('카드 페이지 마운트');

  // 카드사 코드 목록 조회
  await fetchCardCompanyCodes();

  // 약간의 지연 후 데이터 조회 (렌더링 완료 후 조회를 위해)
  setTimeout(() => {
    fetchCardTransactions();
    // 월별 통계 데이터 가져오기 (선택한 월과 상관없이 전체 데이터 기반)
    fetchAllMonthlyStats();
  }, 100);
});

// selectedCardCompany 변경 시 데이터 재조회
watch(selectedCardCompany, () => {
  fetchCardTransactions();
});

// selectedYear 변경 시 데이터 재조회
watch(selectedYear, () => {
  fetchCardTransactions();
});

// selectedMonth 변경 시 데이터 재조회
watch(selectedMonth, () => {
  fetchCardTransactions();
});
</script>

<style scoped>
.max-width-200 {
  max-width: 200px;
}
</style>