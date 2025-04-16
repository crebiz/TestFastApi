<template>
  <div>
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" elevation="2">
          <v-card-text>
            <div class="text-overline text-grey">사용자</div>
            <div class="text-h4 mb-2">{{ stats.userCount }}</div>
            <v-icon color="primary" class="mr-2">mdi-account-group</v-icon>
            <span class="text-caption text-grey">활성 사용자</span>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" elevation="2">
          <v-card-text>
            <div class="text-overline text-grey">방문</div>
            <div class="text-h4 mb-2">{{ stats.visitCount }}</div>
            <v-icon color="success" class="mr-2">mdi-chart-line</v-icon>
            <span class="text-caption text-grey">오늘 방문자</span>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" elevation="2">
          <v-card-text>
            <div class="text-overline text-grey">펀드</div>
            <div class="text-h4 mb-2">{{ stats.fundCount }}</div>
            <v-icon color="info" class="mr-2">mdi-cash-multiple</v-icon>
            <span class="text-caption text-grey">활성 펀드</span>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" lg="3">
        <v-card class="mx-auto" elevation="2">
          <v-card-text>
            <div class="text-overline text-grey">성과</div>
            <div class="text-h4 mb-2">{{ stats.performance }}%</div>
            <v-icon :color="stats.performanceColor" class="mr-2">{{ stats.performanceIcon }}</v-icon>
            <span class="text-caption text-grey">전월 대비</span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-chart-timeline-variant</v-icon>
            월별 통계
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
      
      <v-col cols="12" md="4">
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-account</v-icon>
            최근 활동
          </v-card-title>
          <v-card-text class="px-0">
            <v-list>
              <v-list-item v-for="(activity, index) in recentActivities" :key="index">
                <v-list-item-avatar>
                  <v-avatar :color="activity.color">
                    <v-icon dark>{{ activity.icon }}</v-icon>
                  </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ activity.title }}</v-list-item-title>
                  <v-list-item-subtitle>{{ activity.time }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-table</v-icon>
            최근 거래 내역
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="transactionHeaders"
              :items="transactions"
              :items-per-page="5"
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
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';

export default defineComponent({
  name: 'DashboardPage',
  
  setup() {
    const authStore = useAuthStore();
    // 사용자 정보 가져오기
    const userName = computed(() => authStore.user?.username || '사용자');
    
    // 대시보드 통계 데이터
    const userCount = ref(254);
    const visitCount = ref(54);
    const fundCount = ref(12);
    const performance = ref(15);
    
    const performanceColor = computed(() => {
      return performance.value >= 0 ? 'success' : 'error';
    });
    
    const performanceIcon = computed(() => {
      return performance.value >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down';
    });
    
    // 최근 활동 데이터
    const recentActivities = [
      { 
        title: '새로운 사용자 가입', 
        time: '방금 전', 
        icon: 'mdi-account-plus', 
        color: 'primary' 
      },
      { 
        title: '새로운 펀드 생성', 
        time: '1시간 전', 
        icon: 'mdi-cash-plus', 
        color: 'success' 
      },
      { 
        title: '시스템 업데이트', 
        time: '3시간 전', 
        icon: 'mdi-update', 
        color: 'info' 
      },
      { 
        title: '보안 알림', 
        time: '어제', 
        icon: 'mdi-shield', 
        color: 'warning' 
      }
    ];
    
    // 거래 내역 테이블 데이터
    const headers = [
      { title: 'ID', key: 'id' },
      { title: '날짜', key: 'date' },
      { title: '이름', key: 'name' },
      { title: '금액', key: 'amount' },
      { title: '상태', key: 'status' }
    ];
    
    const transactions = [
      {
        id: '1',
        date: '2025-04-16',
        name: '김철수',
        amount: '₩1,500,000',
        status: '완료'
      },
      {
        id: '2',
        date: '2025-04-15',
        name: '이영희',
        amount: '₩2,300,000',
        status: '대기중'
      },
      {
        id: '3',
        date: '2025-04-14',
        name: '박지민',
        amount: '₩850,000',
        status: '완료'
      },
      {
        id: '4',
        date: '2025-04-13',
        name: '최동욱',
        amount: '₩3,200,000',
        status: '취소'
      },
      {
        id: '5',
        date: '2025-04-12',
        name: '정수민',
        amount: '₩1,750,000',
        status: '완료'
      }
    ];
    
    const getStatusColor = (status: string) => {
      if (status === '완료') return 'success';
      if (status === '대기중') return 'warning';
      if (status === '취소') return 'error';
      return 'grey';
    };
    
    return {
      stats: {
        userCount,
        visitCount,
        fundCount,
        performance,
        performanceColor,
        performanceIcon
      },
      recentActivities,
      transactions,
      transactionHeaders: headers,
      getStatusColor,
      userName
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
