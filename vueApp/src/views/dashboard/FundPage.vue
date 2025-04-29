<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4" elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg pa-3">
            <v-icon class="mr-2 ml-2">mdi-cash-multiple</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">펀드 관리</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn variant="elevated" color="white" class="text-primary mr-2">
              <v-icon left>mdi-plus</v-icon>
              새 펀드 생성
            </v-btn>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-card elevation="2" class="rounded-lg" height="100%">
                  <v-card-text class="pa-4">
                    <div class="d-flex align-center mb-2">
                      <v-avatar color="primary" size="42" class="mr-3">
                        <v-icon color="white">mdi-chart-box</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-grey-darken-1 font-weight-medium">총 펀드 수</div>
                        <div class="text-h4 font-weight-bold">{{ totalFunds }}</div>
                      </div>
                    </div>
                    <v-divider class="my-3"></v-divider>
                    <div class="d-flex align-center">
                      <v-icon color="primary" size="small" class="mr-1">mdi-information</v-icon>
                      <span class="text-caption text-grey-darken-1">활성 펀드</span>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card elevation="2" class="rounded-lg" height="100%">
                  <v-card-text class="pa-4">
                    <div class="d-flex align-center mb-2">
                      <v-avatar color="success" size="42" class="mr-3">
                        <v-icon color="white">mdi-currency-krw</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-grey-darken-1 font-weight-medium">총 투자금</div>
                        <div class="text-h4 font-weight-bold">{{ totalInvestment }}</div>
                      </div>
                    </div>
                    <v-divider class="my-3"></v-divider>
                    <div class="d-flex align-center">
                      <v-icon color="success" size="small" class="mr-1">mdi-information</v-icon>
                      <span class="text-caption text-grey-darken-1">전체 펀드</span>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card elevation="2" class="rounded-lg" height="100%">
                  <v-card-text class="pa-4">
                    <div class="d-flex align-center mb-2">
                      <v-avatar :color="returnColor" size="42" class="mr-3">
                        <v-icon color="white">{{ returnIcon }}</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-grey-darken-1 font-weight-medium">평균 수익률</div>
                        <div class="text-h4 font-weight-bold">{{ averageReturn }}%</div>
                      </div>
                    </div>
                    <v-divider class="my-3"></v-divider>
                    <div class="d-flex align-center">
                      <v-icon :color="returnColor" size="small" class="mr-1">mdi-information</v-icon>
                      <span class="text-caption text-grey-darken-1">전체 펀드</span>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card elevation="2" class="rounded-lg" height="100%">
                  <v-card-text class="pa-4">
                    <div class="d-flex align-center mb-2">
                      <v-avatar color="info" size="42" class="mr-3">
                        <v-icon color="white">mdi-account-group</v-icon>
                      </v-avatar>
                      <div>
                        <div class="text-caption text-grey-darken-1 font-weight-medium">투자자 수</div>
                        <div class="text-h4 font-weight-bold">{{ totalInvestors }}</div>
                      </div>
                    </div>
                    <v-divider class="my-3"></v-divider>
                    <div class="d-flex align-center">
                      <v-icon color="info" size="small" class="mr-1">mdi-information</v-icon>
                      <span class="text-caption text-grey-darken-1">활성 투자자</span>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg pa-3">
            <v-icon class="mr-2 ml-2">mdi-view-list</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">펀드 목록</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="검색" single-line hide-details dense dark
              class="mt-3 max-width-200 mr-2" style="max-width: 200px"></v-text-field>
          </v-toolbar>
          <div class="pa-4">
            <v-sheet rounded="lg" class="pa-4 mb-4 bg-grey-lighten-4">
              <div class="d-flex flex-wrap gap-2">
                <v-chip-group v-model="selectedType" mandatory selected-class="primary">
                  <v-chip v-for="(type, index) in fundTypes" :key="index" :value="type.value" filter variant="elevated"
                    color="primary" height="42" class="ma-1 rounded">
                    <v-icon start>{{ type.icon }}</v-icon>
                    {{ type.label }}
                  </v-chip>
                </v-chip-group>
              </div>
            </v-sheet>

            <div class="d-flex align-center mb-3">
              <v-icon color="primary" size="small" class="mr-2">mdi-information-outline</v-icon>
              <span class="text-subtitle-2 font-weight-medium">총 {{ funds.length }}건의 펀드</span>
              <v-spacer></v-spacer>
            </div>

            <v-divider class="mb-3"></v-divider>
            <v-data-table name="fundTable" :headers="headers" :items="funds" :search="search" :items-per-page="-1"
              :loading="isLoading" class="rounded-lg" item-key="id" hover
              :footer-props="{ 'items-per-page-options': [5, 10, 15, 20, -1] }">
              <template #headers>
                <tr>
                  <th v-for="header in headers" :key="header.value" class="text-primary font-weight-bold">
                    {{ header.text }}
                  </th>
                </tr>
              </template>
              <template #item="{ item, index }">
                <tr @click="viewFund(item)" style="cursor: pointer;">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.fund_nm }}</td>
                  <td>{{ item.financial_comp }}</td>
                  <td>{{ item.account_num }}</td>
                  <td>{{ item.invest_type || '정보 없음' }}</td>
                  <td class="text-truncate" style="max-width: 350px;">
                    <v-tooltip location="top" max-width="500">
                      <template v-slot:activator="{ props }">
                        <span v-bind="props">{{ item.note || '없음' }}</span>
                      </template>
                      <span>{{ item.note || '참고사항이 없습니다.' }}</span>
                    </v-tooltip>
                  </td>
                  <td>
                    <v-chip :color="getStatusColor(item.state)" size="small" @click.stop="deleteFund(item)"
                      :key="item.state" label>
                      {{ item.state }}
                    </v-chip>
                  </td>
                </tr>
              </template>
              <template #bottom>
                <div class="pa-2 d-flex align-center">
                  <span class="text-caption text-grey-darken-1">
                    * 펀드를 클릭하면 상세 정보를 볼 수 있습니다.
                  </span>
                </div>
              </template>
            </v-data-table>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg pa-3">
            <v-icon class="mr-2 ml-2">mdi-chart-pie</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">펀드 분포</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon variant="text" class="mr-2">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-sheet rounded="lg" class="pa-4 bg-grey-lighten-4 mb-4">
              <div class="d-flex align-center mb-2">
                <v-icon color="primary" class="mr-2">mdi-information-outline</v-icon>
                <span class="text-body-2 font-weight-medium">펀드 유형별 분포도</span>
              </div>
            </v-sheet>
            <div class="chart-container" style="height: 300px; position: relative;">
              <div v-if="isChartLoading" class="chart-placeholder d-flex align-center justify-center rounded-lg">
                <div class="text-center">
                  <v-progress-circular indeterminate color="primary" class="mb-3"></v-progress-circular>
                  <div class="text-subtitle-1 text-grey-darken-1">차트 데이터 로딩 중...</div>
                </div>
              </div>
              <div v-else class="h-100">
                <DoughnutChart :data="chartData" :options="chartOptions" />
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="primary" dark class="rounded-t-lg pa-3">
            <v-icon class="mr-2 ml-2">mdi-chart-line</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">펀드 성과 추이</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon variant="text" class="mr-2">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-sheet rounded="lg" class="pa-4 bg-grey-lighten-4 mb-4">
              <div class="d-flex align-center mb-2">
                <v-icon color="primary" class="mr-2">mdi-information-outline</v-icon>
                <span class="text-body-2 font-weight-medium">최근 6개월 수익률 추이</span>
              </div>
            </v-sheet>
            <div class="chart-container" style="height: 300px; position: relative;">
              <div v-if="isChartLoading" class="chart-placeholder d-flex align-center justify-center rounded-lg">
                <div class="text-center">
                  <v-progress-circular indeterminate color="primary" class="mb-3"></v-progress-circular>
                  <div class="text-subtitle-1 text-grey-darken-1">차트 데이터 로딩 중...</div>
                </div>
              </div>
              <div v-else class="h-100">
                <DoughnutChart :data="chartData" :options="chartOptions" />
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 펀드 상세 슬라이드 패널 -->
    <v-navigation-drawer v-model="fundDialog" location="right" temporary width="520" class="fund-detail-drawer"
      elevation="24">
      <v-card flat class="h-100" style="border-radius: 0">
        <v-toolbar flat dark class="pa-3">
          <v-toolbar-title class="text-h6 font-weight-medium ml-2 text-truncate">
            펀드 상세 정보
          </v-toolbar-title>
          <v-btn icon @click="cancelEdit()" class="mr-2">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text v-if="selectedFund" class="pa-6">
          <v-sheet rounded class="pa-4 mb-6 bg-grey-lighten-4">
            <div class="d-flex align-center mb-2">
              <v-avatar color="primary" size="36" class="mr-3">
                <v-icon color="white">mdi-bank</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold">{{ selectedFund.fund_nm }}</div>
                <div class="text-caption text-grey">ID: {{ selectedFund.id }}</div>
              </div>
              <v-spacer></v-spacer>
              <v-chip :color="getStatusColor(selectedFund.state)" label>
                {{ selectedFund.state }}
              </v-chip>
            </div>
          </v-sheet>

          <v-card flat class="mb-4 px-2">
            <v-list>
              <!-- 펀드명 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="primary" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-account-cash</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">펀드명</v-list-item-title>
                <template v-slot:append>
                  <div v-if="!isEditing" class="text-body-1">{{ selectedFund.fund_nm }}</div>
                  <v-text-field v-else v-model="editedFund.fund_nm" variant="outlined" density="compact" hide-details
                    class="edit-field"></v-text-field>
                </template>
              </v-list-item>

              <v-divider></v-divider>

              <!-- 금융사 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="indigo" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-bank</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">금융사</v-list-item-title>
                <template v-slot:append>
                  <div v-if="!isEditing" class="text-body-1">{{ selectedFund.financial_comp }}</div>
                  <v-text-field v-else v-model="editedFund.financial_comp" variant="outlined" density="compact"
                    hide-details class="edit-field"></v-text-field>
                </template>
              </v-list-item>

              <v-divider></v-divider>

              <!-- 유형 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="teal" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-tag</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">유형</v-list-item-title>
                <template v-slot:append>
                  <div v-if="!isEditing" class="text-body-1">
                    {{ getFundTypeLabel(selectedFund.type) }}
                  </div>
                  <v-select v-else v-model="editedFund.type" :items="fundTypes" item-title="label" item-value="value"
                    variant="outlined" density="compact" hide-details class="edit-field">
                    <template v-slot:selection="{ item }">
                      <div class="d-flex align-center text-truncate">
                        <span class="text-truncate">{{ item.raw.label }}</span>
                      </div>
                    </template>
                  </v-select>
                </template>
              </v-list-item>

              <v-divider></v-divider>

              <!-- 투자유형 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="deep-purple" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-chart-box-outline</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">투자유형</v-list-item-title>
                <template v-slot:append>
                  <div v-if="!isEditing" class="text-body-1">{{ selectedFund.invest_type || '정보 없음' }}</div>
                  <v-select v-else v-model="editedFund.invest_type" :items="investTypes" variant="outlined"
                    density="compact" hide-details class="edit-field"></v-select>
                </template>
              </v-list-item>

              <v-divider></v-divider>

              <!-- 생성일 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="amber" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-calendar</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">생성일</v-list-item-title>
                <template v-slot:append>
                  <div class="text-body-1">{{ formatDate(selectedFund.created_at) }}</div>
                </template>
              </v-list-item>

              <v-divider></v-divider>

              <!-- 최근 수정일 -->
              <v-list-item density="compact" class="py-3">
                <template v-slot:prepend>
                  <v-avatar color="blue-grey" size="32" class="mr-3">
                    <v-icon color="white" size="small">mdi-update</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-2 font-weight-medium">최근 수정일</v-list-item-title>
                <template v-slot:append>
                  <div class="text-body-1">{{ formatDate(selectedFund.updated_at) }}</div>
                </template>
              </v-list-item>
            </v-list>
          </v-card>

          <v-divider class="my-4"></v-divider>

          <v-sheet rounded class="pa-4 bg-grey-lighten-5">
            <div class="text-subtitle-2 font-weight-medium mb-2 mt-2">참고사항</div>
            <div v-if="!isEditing" class="text-body-2 text-grey-darken-1">
              {{ selectedFund.note || '참고사항이 없습니다.' }}
            </div>
            <v-textarea v-else v-model="editedFund.note" variant="outlined" density="compact" hide-details
              placeholder="참고사항을 입력하세요" rows="5" class="mt-1 edit-field"></v-textarea>
          </v-sheet>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="cancelEdit()">
            {{ isEditing ? '취소' : '닫기' }}
          </v-btn>
          <v-btn v-if="!isEditing" color="primary" variant="elevated" @click="startEdit">
            <v-icon left>mdi-pencil</v-icon>
            수정
          </v-btn>
          <v-btn v-if="isEditing" color="primary" variant="elevated" @click="saveFund">
            <v-icon left>mdi-content-save</v-icon>
            저장
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-navigation-drawer>
  </div>

  <!-- 스낵바 컴포넌트 -->
  <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" location="top">
    {{ snackbarText }}
    <template v-slot:actions>
      <v-btn variant="text" icon="mdi-close" @click="snackbar = false"></v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from 'chart.js';
import { Doughnut } from 'vue-chartjs';
import { getApiUrl } from '@/config/api';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

interface Fund {
  id: string;
  fund_nm: string;
  created_at: string;
  financial_comp: string;
  type: string;
  account_num: string;
  state: string;
  invest_type: string;
  note: string | null;
  updated_at: string;
}

export default defineComponent({
  name: 'FundPage',
  components: {
    DoughnutChart: Doughnut,
  },

  setup() {
    // 펀드 통계 데이터
    const totalFunds = ref(0);
    const totalInvestment = ref('₩0');
    const averageReturn = ref(0);
    const totalInvestors = ref(0);

    const returnColor = computed(() => {
      return averageReturn.value >= 0 ? 'success' : 'error';
    });

    const returnIcon = computed(() => {
      return averageReturn.value >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down';
    });

    // 펀드 테이블 데이터
    const search = ref('');
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const headers = [
      { text: '번호', value: 'index', width: '60px' },
      { text: '펀드 이름', value: 'fund_nm', width: '180px' },
      { text: '금융사 이름', value: 'financial_comp', width: '120px' },
      { text: '계좌 번호', value: 'account_num', width: '120px' },
      { text: '투자 유형', value: 'invest_type', width: '100px' },
      { text: '참고', value: 'note', width: '350px' },
      { text: '펀드 상태', value: 'state', width: '80px' },
    ];

    const funds = ref<Fund[]>([]);

    // 펀드 데이터 정렬 함수
    const sortFunds = (fundsToSort: Fund[]) => {
      return [...fundsToSort].sort((a, b) => {
        // 먼저 펀드상태별로 정렬 (active가 우선)
        if (a.state !== b.state) {
          return a.state === 'active' ? -1 : 1;
        }

        // 펀드상태가 같으면 투자유형별로 정렬
        if (a.invest_type && b.invest_type) {
          if (a.invest_type < b.invest_type) return -1;
          if (a.invest_type > b.invest_type) return 1;
        } else if (a.invest_type) {
          return -1; // a만 invest_type이 있으면 a가 먼저
        } else if (b.invest_type) {
          return 1; // b만 invest_type이 있으면 b가 먼저
        }

        // 투자유형이 같으면 펀드명으로 정렬
        return a.fund_nm.localeCompare(b.fund_nm, 'ko');
      });
    };

    // 백엔드에서 펀드 데이터 가져오기
    const fetchFunds = async (type: string) => {
      isLoading.value = true;
      error.value = null;

      try {
        const response = await axios.get(getApiUrl(`/funds/?type=${type}`));
        // 데이터를 가져온 후 정렬 함수 적용
        funds.value = sortFunds(response.data);

        // 통계 업데이트
        // totalFunds.value = funds.value.length;
      } catch (err) {
        console.error('펀드 데이터를 가져오는 중 오류 발생:', err);
        error.value = '펀드 데이터를 불러오는 데 실패했습니다.';
      } finally {
        isLoading.value = false;
      }
    };

    const fetchTotalFunds = async () => {
      isLoading.value = true;
      error.value = null;

      try {
        const response = await axios.get(getApiUrl('/funds/total'));
        console.log(response.data);
        totalFunds.value = response.data.length;
      } catch (err) {
        console.error('펀드 데이터를 가져오는 중 오류 발생:', err);
      } finally {
        isLoading.value = false;
      }
    }

    // 컴포넌트 마운트 시 데이터 가져오기
    onMounted(() => {
      fetchTotalFunds();
      fetchFunds('P'); //P:개인연금, W:퇴직연금, F:펀드투자
      fetchInvestTypeDistribution();
    });

    const getStatusColor = (status: string) => {
      if (status === 'active') return 'success';
      if (status === 'inactive') return 'warning';
      return 'grey';
    };

    const getFundTypeLabel = (typeValue: string) => {
      const fundType = fundTypes.value.find(type => type.value === typeValue);
      return fundType ? fundType.label : typeValue;
    };

    // 날짜 포맷 변환 (yyyymmddhhmmss -> yyyy-mm-dd)
    const formatDate = (dateStr: string) => {
      if (!dateStr || dateStr.length < 8) return dateStr;
      const year = dateStr.substring(0, 4);
      const month = dateStr.substring(4, 6);
      const day = dateStr.substring(6, 8);
      return `${year}-${month}-${day}`;
    };

    // 펀드 상세 정보 다이얼로그
    const fundDialog = ref(false);
    const selectedFund = ref<Fund | null>(null);
    const isEditing = ref(false);
    const editedFund = ref<Partial<Fund>>({});
    const fundTypes = ref([
      { value: '', label: '전체', icon: 'mdi-home' },
      { value: 'P', label: '개인연금', icon: 'mdi-account-cash' },
      { value: 'W', label: '퇴직연금', icon: 'mdi-briefcase-outline' },
      { value: 'F', label: '펀드투자', icon: 'mdi-chart-box-outline' },
      { value: 'O', label: '해외펀드', icon: 'mdi-earth' }
    ]);

    const investTypes = ref([
      '일반주식',
      '글로벌주식',
      '아시아태평양주식',
      '북미주식',
      '유럽주식',
      '일본주식',
      '인도주식',
      '베트남주식',
      '배당주식',
      '정보기술',
      '기초소재',
      '금융',
      '기타인덱스',
      '신흥국채권',
      '글로벌채권',
      '글로벌리츠재간접',
      '글로벌하이일드채권',
      '글로벌라이프싸이클',
      '글로벌보수적자산배분'
    ]);

    const selectedType = ref('P');

    watch(selectedType, (newType: string) => {
      fetchFunds(newType);
    });

    const viewFund = (fund: Fund | any) => {
      console.log('Viewing fund:', fund);
      selectedFund.value = fund;
      fundDialog.value = true;
    };

    const startEdit = () => {
      // 수정 모드 시작
      isEditing.value = true;

      // 현재 선택된 펀드 정보를 복사하여 수정용 객체에 저장
      if (selectedFund.value) {
        editedFund.value = { ...selectedFund.value };
        // 펀드 유형 설정
        // selectedFund.value가 null이 아님을 확인했으므로 안전하게 접근 가능
        const typeValue = selectedFund.value.type;
        editedFund.value.type = typeValue;
      }
    };

    const cancelEdit = () => {
      // 수정 모드 취소
      if (isEditing.value) {
        isEditing.value = false;
        editedFund.value = {}; // 수정 내용 초기화
      } else {
        // 수정 모드가 아닌 경우 다이얼로그 닫기
        fundDialog.value = false;
        // 현재 선택된 펀드의 타입으로 목록 새로고침
        if (selectedFund.value && selectedFund.value.type) {
          fetchFunds(selectedFund.value.type);
        } else {
          fetchFunds(selectedType.value);
        }
      }
    };

    const saveFund = async () => {
      // 수정된 내용이 있는지 확인
      if (!selectedFund.value || !editedFund.value) return;

      // 변경된 필드 확인
      const changes: Partial<Fund> = {};
      let hasChanges = false;

      // 각 필드별로 변경 사항 확인
      Object.keys(editedFund.value).forEach((key) => {
        const k = key as keyof Fund;
        if (editedFund.value[k] !== selectedFund.value?.[k]) {
          // @ts-expect-error - Fund 타입에 대한 동적 키 접근
          changes[k] = editedFund.value[k];
          hasChanges = true;
        }
      });

      if (!hasChanges) {
        // 스낵바로 메시지 표시
        snackbarText.value = '수정된 내용이 없습니다.';
        snackbarColor.value = 'info';
        snackbar.value = true;
        return;
      }

      try {
        isLoading.value = true;
        // 백엔드 API 호출
        const response = await axios.put(`http://localhost:8000/funds/${selectedFund.value.id}`, changes);

        // 응답 데이터로 선택된 펀드 정보 업데이트
        selectedFund.value = response.data;

        // 목록에서도 해당 펀드 정보 업데이트
        const index = funds.value.findIndex(f => f.id === selectedFund.value?.id);
        if (index !== -1 && selectedFund.value) {
          funds.value[index] = { ...selectedFund.value };
        }

        // 수정 모드 종료
        isEditing.value = false;
        // 스낵바로 성공 메시지 표시
        snackbarText.value = '펀드 정보가 성공적으로 업데이트되었습니다.';
        snackbarColor.value = 'success';
        snackbar.value = true;

        // 유형이 변경되었는지 확인
        if (changes.type && changes.type !== selectedType.value) {
          // 변경된 유형으로 선택된 타입 업데이트
          selectedType.value = changes.type;
          // 변경된 유형으로 목록 새로고침
          fetchFunds(changes.type);
        }
      } catch (error) {
        console.error('펀드 정보 업데이트 중 오류 발생:', error);
        // 스낵바로 오류 메시지 표시
        snackbarText.value = '펀드 정보 업데이트 중 오류가 발생했습니다.';
        snackbarColor.value = 'error';
        snackbar.value = true;
      } finally {
        isLoading.value = false;
      }
    };

    const deleteFund = async (fund: Fund) => {
      try {
        isLoading.value = true;
        console.log('토글 펀드 상태:', fund.id, fund.state);

        // 백엔드 API 호출하여 펀드 상태 토글
        const response = await axios.put(`http://localhost:8000/funds/${fund.id}/toggle-state`);

        // 응답에서 업데이트된 펀드 정보 가져오기
        const updatedFund = response.data;
        console.log('상태 변경 완료:', updatedFund);

        // 로컬 펀드 목록 업데이트
        const index = funds.value.findIndex(f => f.id === fund.id);
        if (index !== -1) {
          // 상태 토글 (active <-> inactive)
          funds.value[index].state = updatedFund.state;

          // 상태 변경 후 다시 정렬
          funds.value = sortFunds(funds.value);
        }

        // 성공 메시지 표시 (선택 사항)
        // alert(`펀드 상태가 ${updatedFund.state}로 변경되었습니다.`);
      } catch (error) {
        console.error('펀드 상태 토글 중 오류 발생:', error);
        // alert('펀드 상태를 변경하는 중 오류가 발생했습니다.');
        snackbarText.value = '펀드 상태를 변경하는 중 오류가 발생했습니다.';
        snackbarColor.value = 'error';
        snackbar.value = true;
      } finally {
        isLoading.value = false;
      }
    };

    // 스낵바 관련 상태
    const snackbar = ref(false);
    const snackbarText = ref('');
    const snackbarColor = ref('success');

    // 차트 관련 상태
    const isChartLoading = ref(true);

    // 차트 데이터 타입 정의
    interface ChartDataType {
      labels: string[];
      datasets: Array<{
        label?: string;
        backgroundColor: string[];
        data: number[];
      }>;
    }

    const chartData = ref<ChartDataType>({
      labels: [],
      datasets: [{
        label: '투자유형별 펀드 수',
        backgroundColor: [
          '#4CAF50', // 초록
          '#2196F3', // 파랑
          '#FFC107', // 노랑
          '#9C27B0', // 보라
          '#FF5722', // 주황
          '#607D8B', // 회색
          '#E91E63', // 핑크
          '#3F51B5', // 남색
          '#009688'  // 청록
        ],
        data: []
      }]
    });

    // 차트 옵션 타입 정의
    interface ChartOptionsType {
      responsive: boolean;
      maintainAspectRatio: boolean;
      plugins: {
        legend: {
          position: 'bottom' | 'center' | 'top' | 'left' | 'right' | 'chartArea';
          labels: {
            font: {
              family: string;
              size: number;
            };
            padding: number;
          };
        };
        tooltip: {
          callbacks: {
            label: (context: any) => string;
          };
        };
      };
      cutout: string;
    }

    const chartOptions = ref<ChartOptionsType>({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: {
              family: '"Noto Sans KR", sans-serif',
              size: 12
            },
            padding: 20
          }
        },
        tooltip: {
          callbacks: {
            label: function (context: any) {
              const label = context.label || '';
              const value = context.raw || 0;
              const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value}개 (${percentage}%)`;
            }
          }
        }
      },
      cutout: '60%' // 도넛 차트의 중앙 구멍 크기
    });

    // 펀드 유형별 분포도 차트 데이터 가져오기
    const fetchInvestTypeDistribution = async () => {
      isChartLoading.value = true;
      try {
        // 전체 펀드 데이터 가져오기
        const response = await axios.get(getApiUrl('/funds/'));
        const allFunds = response.data;

        // 투자유형별 분포 계산
        const distribution: Record<string, number> = {};

        // 초기화: 모든 투자유형에 대해 0으로 초기화
        investTypes.value.forEach(type => {
          distribution[type] = 0;
        });

        // 투자유형이 없는 펀드를 위한 추가 버킷
        distribution['지정되지 않음'] = 0;

        // 각 펀드의 투자유형 카운트
        allFunds.forEach((fund: any) => {
          if (fund.invest_type) {
            distribution[fund.invest_type] = (distribution[fund.invest_type] || 0) + 1;
          } else {
            distribution['지정되지 않음']++;
          }
        });

        // 차트 데이터 형식으로 변환
        const chartEntries: [string, number][] = [];

        // 0이 아닌 값만 필터링
        Object.entries(distribution).forEach(([type, count]: [string, number]) => {
          if (count > 0) {
            chartEntries.push([type, count]);
          }
        });

        // 건수가 많은 순으로 정렬
        chartEntries.sort((a, b) => b[1] - a[1]);

        // 정렬된 데이터로 라벨과 데이터 배열 생성
        const labels: string[] = chartEntries.map(entry => entry[0]);
        const data: number[] = chartEntries.map(entry => entry[1]);

        // 차트 데이터 업데이트
        chartData.value = {
          labels: labels,
          datasets: [{
            label: '투자유형별 펀드 수',
            backgroundColor: [
              '#4CAF50', // 초록
              '#2196F3', // 파랑
              '#FFC107', // 노랑
              '#9C27B0', // 보라
              '#FF5722', // 주황
              '#607D8B', // 회색
              '#E91E63', // 핑크
              '#3F51B5', // 남색
              '#009688'  // 청록
            ],
            data: data
          }]
        };
      } catch (error) {
        console.error('투자유형별 분포도 데이터 가져오기 오류:', error);
        snackbarText.value = '차트 데이터를 불러오는 중 오류가 발생했습니다.';
        snackbarColor.value = 'error';
        snackbar.value = true;
      } finally {
        isChartLoading.value = false;
      }
    };

    return {
      totalFunds,
      totalInvestment,
      averageReturn,
      totalInvestors,
      returnColor,
      returnIcon,
      search,
      headers,
      funds,
      isLoading,
      error,
      getStatusColor,
      formatDate,
      fundDialog,
      selectedFund,
      selectedType,
      fundTypes,
      investTypes,
      getFundTypeLabel,
      viewFund,
      isEditing,
      editedFund,
      startEdit,
      cancelEdit,
      saveFund,
      deleteFund,
      fetchFunds,
      fetchTotalFunds,
      // 스낵바 관련 변수
      snackbar,
      snackbarText,
      snackbarColor,
      // 차트 관련 변수
      isChartLoading,
      chartData,
      chartOptions,
    };
  }
});
</script>

<style scoped>
.chart-placeholder {
  height: 100%;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.card-inner-padding {
  padding-left: 24px;
  padding-right: 24px;
  padding-top: 0;
  padding-bottom: 0;
}

.fund-card-container {
  border: 1px solid;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.border-green {
  border-color: #8fc7a3 !important;
}

.gap-2 {
  gap: 8px;
}

.btn-mingl-outline {
  border: 1.5px solid #c2e3d1 !important;
  border-radius: 20px !important;
  color: #388e5c !important;
  background-color: white !important;
  font-weight: 500;
  min-width: 90px;
  transition: all 0.2s ease;
  margin: 0 4px;
}

.btn-mingl-outline:hover {
  background-color: #f0f8f4 !important;
}

.btn-mingl-outline.active {
  background: #137c54 !important;
  color: white !important;
  border-color: #137c54 !important;
}

.fund-type-toggle {
  border: 2px solid #8fc7a3;
  border-radius: 12px;
  padding: 16px 24px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  margin: 0;
  height: 66px;
}

.edit-field {
  width: 100%;
  min-width: 250px;
  max-width: 480px;
}

.single-line-select :deep(.v-field__input) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.single-line-select :deep(.v-select__selection) {
  max-width: 100%;
  overflow: hidden;
}

.fund-type-btn {
  min-width: 90px;
  margin: 0 8px;
  border-radius: 20px !important;
  background: #fff !important;
  color: #388e5c !important;
  border: 1.5px solid #c2e3d1 !important;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
  line-height: 32px;
  padding-top: 0;
  padding-bottom: 0;
  box-sizing: border-box;
}

.fund-type-btn.active {
  background: #137c54 !important;
  color: #fff !important;
  border: 1.5px solid #137c54 !important;
}


.chart-placeholder {
  height: 100%;
  background-color: #f9f9f9;
  border-radius: 4px;
}
</style>