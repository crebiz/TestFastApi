<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4" elevation="2">
          <v-card-title class="d-flex justify-space-between align-center">
            <div>
              <v-icon left color="primary">mdi-cash-multiple</v-icon>
              펀드 관리
            </div>
            <v-btn color="primary">
              <v-icon left>mdi-plus</v-icon>
              새 펀드 생성
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-card outlined>
                  <v-card-text>
                    <div class="text-overline text-grey">총 펀드 수</div>
                    <div class="text-h4 mb-2">{{ totalFunds }}</div>
                    <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
                    <span class="text-caption text-grey">활성 펀드</span>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card outlined>
                  <v-card-text>
                    <div class="text-overline text-grey">총 투자금</div>
                    <div class="text-h4 mb-2">{{ totalInvestment }}</div>
                    <v-icon color="success" class="mr-2">mdi-currency-krw</v-icon>
                    <span class="text-caption text-grey">전체 펀드</span>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card outlined>
                  <v-card-text>
                    <div class="text-overline text-grey">평균 수익률</div>
                    <div class="text-h4 mb-2">{{ averageReturn }}%</div>
                    <v-icon :color="returnColor" class="mr-2">{{ returnIcon }}</v-icon>
                    <span class="text-caption text-grey">전체 펀드</span>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-card outlined>
                  <v-card-text>
                    <div class="text-overline text-grey">투자자 수</div>
                    <div class="text-h4 mb-2">{{ totalInvestors }}</div>
                    <v-icon color="info" class="mr-2">mdi-account-group</v-icon>
                    <span class="text-caption text-grey">활성 투자자</span>
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
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-view-list</v-icon>
            펀드 목록
            <v-spacer></v-spacer>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="검색" single-line hide-details class="ml-4"
              style="max-width: 300px;"></v-text-field>
          </v-card-title>

          <v-data-table :headers="headers" :items="funds" :search="search" :items-per-page="10" :loading="isLoading"
            class="elevation-0" item-key="id">
            <template v-slot:[`item.index`]="{ index }">
              {{ index + 1 }}
            </template>
            
            <template v-slot:[`item.state`]="{ item }">
              <v-chip :color="getStatusColor(item.state)" small>
                {{ item.state }}
              </v-chip>
            </template>

            <template v-slot:[`item.created_at`]="{ item }">
              {{ formatDate(item.created_at) }}
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-btn icon small class="mr-1" @click="viewFund(item)">
                <v-icon small>mdi-eye</v-icon>
              </v-btn>
              <v-btn icon small class="mr-1" @click="editFund(item)">
                <v-icon small>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon small @click="deleteFund(item)">
                <v-icon small>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-chart-pie</v-icon>
            펀드 분포
          </v-card-title>
          <v-card-text>
            <div class="chart-container" style="height: 300px; position: relative;">
              <div class="chart-placeholder d-flex align-center justify-center">
                <span class="text-subtitle-1 text-grey">차트 데이터 로딩 중...</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-chart-line</v-icon>
            펀드 성과 추이
          </v-card-title>
          <v-card-text>
            <div class="chart-container" style="height: 300px; position: relative;">
              <div class="chart-placeholder d-flex align-center justify-center">
                <span class="text-subtitle-1 text-grey">차트 데이터 로딩 중...</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 펀드 상세 다이얼로그 -->
    <v-dialog v-model="fundDialog" max-width="800">
      <v-card>
        <v-card-title class="headline">
          {{ selectedFund ? selectedFund.fund_nm : '펀드 상세 정보' }}
          <v-spacer></v-spacer>
          <v-btn icon @click="fundDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text v-if="selectedFund">
          <v-row>
            <v-col cols="12" md="6">
              <div class="text-overline text-grey">펀드 ID</div>
              <div class="text-body-1 mb-2">{{ selectedFund.id }}</div>

              <div class="text-overline text-grey">펀드명</div>
              <div class="text-body-1 mb-2">{{ selectedFund.fund_nm }}</div>

              <div class="text-overline text-grey">생성일</div>
              <div class="text-body-1 mb-2">{{ formatDate(selectedFund.created_at) }}</div>

              <div class="text-overline text-grey">금융사</div>
              <div class="text-body-1 mb-2">{{ selectedFund.financial_comp }}</div>
            </v-col>

            <v-col cols="12" md="6">
              <div class="text-overline text-grey">펀드 종류</div>
              <div class="text-body-1 mb-2">
                {{ selectedFund.type }}
              </div>

              <div class="text-overline text-grey">계좌번호</div>
              <div class="text-body-1 mb-2">{{ selectedFund.account_num }}</div>

              <div class="text-overline text-grey">상태</div>
              <div class="text-body-1 mb-2">
                <v-chip :color="getStatusColor(selectedFund.state)" small>{{ selectedFund.state }}</v-chip>
              </div>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">투자 금액</v-list-item-subtitle>
                    <v-list-item-title>{{ selectedFund.amount }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">수익률</v-list-item-subtitle>
                    <v-list-item-title>
                      <span :class="selectedFund.return >= 0 ? 'success--text' : 'error--text'">
                        {{ selectedFund.return }}%
                      </span>
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">투자자 수</v-list-item-subtitle>
                    <v-list-item-title>{{ selectedFund.investors }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="text-overline text-grey">수정일</div>
          <div class="text-body-1">{{ formatDate(selectedFund.updated_at) }}</div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="fundDialog = false">
            닫기
          </v-btn>
          <v-btn color="primary" @click="editFund(selectedFund)">
            수정
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import axios from 'axios';

interface Fund {
  id: string;
  fund_nm: string;
  created_at: string;
  financial_comp: string;
  type: string;
  account_num: string;
  state: string;
  updated_at: string;
}

export default defineComponent({
  name: 'FundPage',

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
      { text: 'No', value: 'index', width: '60px' },
      { text: '펀드명', value: 'fund_nm', width: '200px' },
      { text: '금융사', value: 'financial_comp', width: '150px' },
      { text: '계좌번호', value: 'account_num', width: '150px' },
      { text: '펀드 종류', value: 'type', width: '120px' },
      { text: '상태', value: 'state', width: '100px' },
      { text: '관리', value: 'actions', sortable: false, width: '120px' }
    ];

    const funds = ref<Fund[]>([]);

    // 백엔드에서 펀드 데이터 가져오기
    const fetchFunds = async () => {
      isLoading.value = true;
      error.value = null;

      try {
        const response = await axios.get('http://localhost:8000/funds/');
        funds.value = response.data;
        console.log(funds.value);

        // 통계 업데이트
        totalFunds.value = funds.value.length;
      } catch (err) {
        console.error('펀드 데이터를 가져오는 중 오류 발생:', err);
        error.value = '펀드 데이터를 불러오는 데 실패했습니다.';
      } finally {
        isLoading.value = false;
      }
    };

    // 컴포넌트 마운트 시 데이터 가져오기
    onMounted(() => {
      fetchFunds();
    });

    const getStatusColor = (status: string) => {
      if (status === 'active') return 'success';
      if (status === 'inactive') return 'warning';
      return 'grey';
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

    const viewFund = (fund: Fund) => {
      selectedFund.value = fund;
      fundDialog.value = true;
    };

    const editFund = (fund: Fund) => {
      // 펀드 수정 로직
      console.log('Edit fund:', fund);
      // 실제로는 수정 폼을 표시하거나 API 호출을 수행
    };

    const deleteFund = (fund: Fund) => {
      // 펀드 삭제 로직
      console.log('Delete fund:', fund);
      // 실제로는 삭제 확인 다이얼로그를 표시하거나 API 호출을 수행
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
      viewFund,
      editFund,
      deleteFund,
      fetchFunds
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
</style>
