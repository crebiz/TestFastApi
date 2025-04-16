<template>
  <div>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="h-100" elevation="3" rounded="lg">
          <v-card-text class="text-center">
            <v-avatar size="150" class="mb-4" color="primary">
              <v-img
                :src="userAvatar"
                alt="User"
              ></v-img>
            </v-avatar>
            <h2 class="text-h5 mb-1">{{ userName }}</h2>
            <p class="text-subtitle-1 text-grey">{{ userEmail }}</p>
            <v-divider class="my-4"></v-divider>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="8">
        <v-card class="h-100" elevation="3" rounded="lg">
          <v-card-title class="text-primary">
            <v-icon left color="secondary">mdi-information</v-icon>
            계정 정보
          </v-card-title>
          <v-card-text>
            <div class="info-grid">
              <div class="info-item">
                <div class="info-icon">
                  <v-icon color="primary">mdi-account</v-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">사용자 ID</div>
                  <div class="info-value">{{ userId }}</div>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-icon">
                  <v-icon color="primary">mdi-google</v-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">Google 계정</div>
                  <div class="info-value">{{ userEmail }}</div>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-icon">
                  <v-icon color="primary">mdi-calendar</v-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">가입일</div>
                  <div class="info-value">{{ joinDate }}</div>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-icon">
                  <v-icon color="primary">mdi-clock</v-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">마지막 로그인</div>
                  <div class="info-value">{{ lastLogin }}</div>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-icon">
                  <v-icon color="primary">mdi-shield</v-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">계정 상태</div>
                  <div class="info-value">
                    <v-chip size="small" color="secondary" text-color="white">활성</v-chip>
                  </div>
                </div>
              </div>
            </div>
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
  name: 'ProfilePage',
  
  setup() {
    const authStore = useAuthStore();
    
    // 사용자 정보
    const userId = ref(authStore.user?.email.split('@')[0] || 1);
    const userName = ref(authStore.user?.username || '사용자');
    const userEmail = ref(authStore.user?.email || 'user@example.com');
    const userAvatar = computed(() => {
      return authStore.user?.imageUrl || 'https://via.placeholder.com/150?text=User';
    });
    
    // 계정 정보
    const joinDate = ref('2025-01-15');
    const lastLogin = ref('2025-04-16 15:30:45');
    
    // 로그인 및 토큰 관련 코드 제거
    
    return {
      userId,
      userName,
      userEmail,
      userAvatar,
      joinDate,
      lastLogin
    };
  }
});
</script>

<style scoped>
/* Material Design 3 스타일 */
.v-card {
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
}

.v-list-item-title {
  font-weight: 500;
  color: var(--v-theme-primary);
}

.v-list-item-subtitle {
  color: rgba(0, 0, 0, 0.6);
}

.v-btn.v-btn--variant-elevated {
  background-color: var(--v-theme-secondary) !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-weight: 500;
}

.h-100 {
  height: 100%;
}

.v-avatar {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 가로 레이아웃 정보 그리드 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 12px;
  background-color: rgba(0, 150, 136, 0.05);
  transition: background-color 0.2s ease;
}

.info-item:hover {
  background-color: rgba(0, 150, 136, 0.1);
}

.info-icon {
  margin-right: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(0, 150, 136, 0.1);
}

.info-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.info-title {
  font-weight: 500;
  color: var(--v-theme-primary);
}

.info-value {
  color: rgba(0, 0, 0, 0.6);
  font-weight: 400;
}
</style>
