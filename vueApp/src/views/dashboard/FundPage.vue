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
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="검색"
              single-line
              hide-details
              class="ml-4"
              style="max-width: 300px;"
            ></v-text-field>
          </v-card-title>
          
          <v-data-table
            :headers="headers"
            :items="funds"
            :search="search"
            :items-per-page="10"
            class="elevation-0"
          >
            <template #item.status="{ item }">
              <v-chip
                :color="getStatusColor(item.status)"
                small
              >
                {{ item.status }}
              </v-chip>
            </template>
            
            <template #item.return="{ item }">
              <span :class="item.return >= 0 ? 'success--text' : 'error--text'">
                <v-icon small :color="item.return >= 0 ? 'success' : 'error'" class="mr-1">
                  {{ item.return >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                </v-icon>
                {{ item.return }}%
              </span>
            </template>
            
            <template #item.actions="{ item }">
              <v-btn icon small class="mr-2" @click="viewFund(item)">
                <v-icon small>mdi-eye</v-icon>
              </v-btn>
              <v-btn icon small class="mr-2" @click="editFund(item)">
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
          {{ selectedFund ? selectedFund.name : '펀드 상세 정보' }}
          <v-spacer></v-spacer>
          <v-btn icon @click="fundDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text v-if="selectedFund">
          <v-row>
            <v-col cols="12" md="6">
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">펀드 ID</v-list-item-subtitle>
                    <v-list-item-title>{{ selectedFund.id }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">생성일</v-list-item-subtitle>
                    <v-list-item-title>{{ selectedFund.createdAt }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-subtitle class="text-overline">상태</v-list-item-subtitle>
                    <v-list-item-title>
                      <v-chip
                        :color="getStatusColor(selectedFund.status)"
                        small
                      >
                        {{ selectedFund.status }}
                      </v-chip>
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-col>
            
            <v-col cols="12" md="6">
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
          
          <h3 class="text-subtitle-1 mb-2">펀드 설명</h3>
          <p>{{ selectedFund.description }}</p>
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
import { defineComponent, ref, computed } from 'vue';

// 펀드 타입 정의
interface Fund {
  id: string;
  name: string;
  createdAt: string;
  amount: string;
  return: number;
  investors: number;
  status: string;
  description: string;
}

export default defineComponent({
  name: 'FundPage',
  
  setup() {
    // 펀드 통계 데이터
    const totalFunds = ref(12);
    const totalInvestment = ref('₩2,450,000,000');
    const averageReturn = ref(8.5);
    const totalInvestors = ref(156);
    
    const returnColor = computed(() => {
      return averageReturn.value >= 0 ? 'success' : 'error';
    });
    
    const returnIcon = computed(() => {
      return averageReturn.value >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down';
    });
    
    // 펀드 테이블 데이터
    const search = ref('');
    
    const headers = [
      { text: 'ID', value: 'id', width: '80px' },
      { text: '펀드명', value: 'name', width: '200px' },
      { text: '생성일', value: 'createdAt', width: '120px' },
      { text: '금액', value: 'amount', width: '150px' },
      { text: '수익률', value: 'return', width: '100px' },
      { text: '투자자 수', value: 'investors', width: '100px' },
      { text: '상태', value: 'status', width: '100px' },
      { text: '관리', value: 'actions', sortable: false, width: '120px' }
    ];
    
    const funds = [
      {
        id: 'F001',
        name: '기술 혁신 펀드',
        createdAt: '2025-01-15',
        amount: '₩500,000,000',
        return: 12.5,
        investors: 45,
        status: '활성',
        description: '이 펀드는 혁신적인 기술 기업에 투자하여 높은 수익을 추구합니다. 인공지능, 블록체인, 로봇공학 등 첨단 기술 분야의 성장 가능성이 높은 기업들을 대상으로 합니다.'
      },
      {
        id: 'F002',
        name: '안정 성장 펀드',
        createdAt: '2025-02-03',
        amount: '₩350,000,000',
        return: 5.8,
        investors: 32,
        status: '활성',
        description: '안정적인 성장을 추구하는 펀드로, 검증된 기업들에 투자하여 중장기적인 수익을 목표로 합니다. 변동성이 낮고 배당금이 높은 기업들을 중심으로 포트폴리오를 구성합니다.'
      },
      {
        id: 'F003',
        name: '신흥 시장 펀드',
        createdAt: '2025-02-18',
        amount: '₩420,000,000',
        return: -2.3,
        investors: 28,
        status: '활성',
        description: '신흥 시장의 성장 잠재력에 투자하는 펀드입니다. 동남아시아, 남미, 아프리카 등 성장 가능성이 높은 지역의 기업들에 투자하여 장기적인 수익을 추구합니다.'
      },
      {
        id: 'F004',
        name: '부동산 투자 펀드',
        createdAt: '2025-03-05',
        amount: '₩650,000,000',
        return: 7.2,
        investors: 51,
        status: '활성',
        description: '상업용 및 주거용 부동산에 투자하는 펀드로, 안정적인 임대 수익과 자산 가치 상승을 통한 수익을 목표로 합니다. 주요 도시의 핵심 지역 부동산을 중심으로 투자합니다.'
      },
      {
        id: 'F005',
        name: '친환경 에너지 펀드',
        createdAt: '2025-03-22',
        amount: '₩280,000,000',
        return: 15.7,
        investors: 24,
        status: '활성',
        description: '재생 에너지, 전기차, 에너지 효율화 기술 등 친환경 에너지 분야에 투자하는 펀드입니다. 지속 가능한 발전과 환경 보호에 기여하면서 높은 수익을 추구합니다.'
      },
      {
        id: 'F006',
        name: '헬스케어 혁신 펀드',
        createdAt: '2025-04-10',
        amount: '₩320,000,000',
        return: 9.3,
        investors: 29,
        status: '활성',
        description: '의료 기술, 바이오테크, 디지털 헬스케어 등 헬스케어 분야의 혁신 기업에 투자하는 펀드입니다. 인구 고령화와 건강에 대한 관심 증가로 성장이 예상되는 분야입니다.'
      },
      {
        id: 'F007',
        name: '스타트업 인큐베이팅 펀드',
        createdAt: '2024-11-15',
        amount: '₩180,000,000',
        return: -5.2,
        investors: 15,
        status: '중지',
        description: '초기 단계의 유망한 스타트업에 투자하여 높은 수익을 추구하는 펀드입니다. 혁신적인 비즈니스 모델과 성장 잠재력이 높은 스타트업을 발굴하고 지원합니다.'
      },
      {
        id: 'F008',
        name: '글로벌 인프라 펀드',
        createdAt: '2024-12-05',
        amount: '₩520,000,000',
        return: 4.8,
        investors: 38,
        status: '완료',
        description: '전 세계의 인프라 프로젝트에 투자하는 펀드로, 도로, 항만, 공항, 에너지 시설 등 사회 기반 시설에 투자하여 안정적인 장기 수익을 추구합니다.'
      }
    ];
    
    const getStatusColor = (status: string) => {
      if (status === '활성') return 'success';
      if (status === '중지') return 'warning';
      if (status === '완료') return 'info';
      return 'grey';
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
      getStatusColor,
      fundDialog,
      selectedFund,
      viewFund,
      editFund,
      deleteFund
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
