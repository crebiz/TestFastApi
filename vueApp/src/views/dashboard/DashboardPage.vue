<template>
  <div class="dashboard-container">
    <v-container fluid style="min-height: 100vh;">
      <div class="px-6 py-4">
        <h1 class="text-h4 font-weight-bold mb-2">Dashboard Overview</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Key metrics and insights at a glance.</p>

        <h2 class="text-h5 font-weight-bold mt-6 mb-4">Overall Performance</h2>
        
        <div class="d-flex align-center">
          <div class="text-h2 font-weight-bold">75%</div>
          <div class="ml-4 text-subtitle-1 text-success">Last 30 Days <span class="font-weight-bold">+5%</span></div>
        </div>
        
        <div class="performance-chart mt-4" style="height: 150px; position: relative;">
          <v-img src="https://via.placeholder.com/1200x150/14171F/2A3042?text=Performance+Chart" height="150" 
            class="rounded-lg" style="opacity: 0.8"></v-img>
        </div>

        <h2 class="text-h5 font-weight-bold mt-8 mb-4">Key Metrics</h2>
        
        <v-row>
          <v-col cols="12" sm="6" lg="4">
            <v-card class="metric-card" color="var(--color-tertiary)" elevation="0" rounded="lg">
              <v-card-text>
                <div class="text-subtitle-1 text-medium-emphasis mb-2">Total Users</div>
                <div class="d-flex align-center justify-space-between">
                  <div class="text-h3 font-weight-bold">1,200</div>
                  <div class="text-success font-weight-medium">+10%</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" sm="6" lg="4">
            <v-card class="metric-card" color="var(--color-tertiary)" elevation="0" rounded="lg">
              <v-card-text>
                <div class="text-subtitle-1 text-medium-emphasis mb-2">Active Users</div>
                <div class="d-flex align-center justify-space-between">
                  <div class="text-h3 font-weight-bold">850</div>
                  <div class="text-success font-weight-medium">+5%</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" sm="6" lg="4">
            <v-card class="metric-card" color="var(--color-tertiary)" elevation="0" rounded="lg">
              <v-card-text>
                <div class="text-subtitle-1 text-medium-emphasis mb-2">Conversion Rate</div>
                <div class="d-flex align-center justify-space-between">
                  <div class="text-h3 font-weight-bold">15%</div>
                  <div class="text-error font-weight-medium">-2%</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      
      <h2 class="text-h5 font-weight-bold mt-8 mb-4">Recent Activities</h2>
        
      <v-card class="activity-card" color="var(--color-tertiary)" elevation="0" rounded="lg">
        <v-card-text>
          <v-list bg-color="transparent">
            <v-list-item v-for="(activity, index) in recentActivities" :key="index" class="pa-0 mb-3">
              <template v-slot:prepend>
                <v-avatar size="42" :color="activity.color" class="mr-3">
                  <v-icon color="white">{{ activity.icon }}</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title class="text-subtitle-1 font-weight-medium">{{ activity.title }}</v-list-item-title>
              <v-list-item-subtitle class="text-caption text-medium-emphasis">{{ activity.time }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
      
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';

export default defineComponent({
  name: 'DashboardPage',
  
  setup() {
    const authStore = useAuthStore();
    // 사용자 정보 가져오기
    const userName = computed(() => authStore.user?.username || 'User');
    
    // 최근 활동 데이터
    const recentActivities = [
      { 
        title: 'New User Registration', 
        time: 'User signed up', 
        icon: 'mdi-account-plus', 
        color: '#3B82F6' 
      },
      { 
        title: 'Weekly Report', 
        time: 'Report generated', 
        icon: 'mdi-file-document-outline', 
        color: '#10B981' 
      },
      { 
        title: 'Project Milestone', 
        time: 'Task completed', 
        icon: 'mdi-flag-checkered', 
        color: '#6366F1' 
      }
    ];
    
    return {
      recentActivities,
      userName
    };
  }
});
</script>

<style scoped>
.dashboard-header {
  color: var(--text-dark);
  font-weight: 600;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.metric-card {
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-dark);
}

.activity-card {
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-dark);
}

.text-success {
  color: var(--color-success) !important;
}

.text-error {
  color: var(--color-error) !important;
}

.text-medium-emphasis {
  opacity: 0.7;
}
</style>
