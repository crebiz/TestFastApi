<template>
  <div>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="mb-4" elevation="2">
          <v-card-text class="text-center">
            <v-avatar size="150" class="mb-4">
              <v-img
                :src="userAvatar"
                alt="User"
              ></v-img>
            </v-avatar>
            <h2 class="text-h5 mb-1">{{ userName }}</h2>
            <p class="text-subtitle-1 text-grey">{{ userEmail }}</p>
            <v-divider class="my-4"></v-divider>
            <v-btn
              color="primary"
              block
              class="mb-2"
            >
              프로필 수정
            </v-btn>
          </v-card-text>
        </v-card>
        
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-information</v-icon>
            계정 정보
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-account</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>사용자 ID</v-list-item-title>
                  <v-list-item-subtitle>{{ userId }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-calendar</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>가입일</v-list-item-title>
                  <v-list-item-subtitle>{{ joinDate }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-clock</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>마지막 로그인</v-list-item-title>
                  <v-list-item-subtitle>{{ lastLogin }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-shield</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>계정 상태</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip small color="success" text-color="white">활성</v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="8">
        <v-card elevation="2" class="mb-4">
          <v-card-title>
            <v-icon left color="primary">mdi-security</v-icon>
            로그인 정보
          </v-card-title>
          <v-card-text>
            <v-alert
              type="info"
              outlined
              class="mb-4"
            >
              Google 계정으로 로그인 중입니다. 계정 정보는 Google에서 관리됩니다.
            </v-alert>
            
            <v-list>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-google</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Google 계정</v-list-item-title>
                  <v-list-item-subtitle>{{ userEmail }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-key</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>액세스 토큰</v-list-item-title>
                  <v-list-item-subtitle>{{ accessTokenMasked }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>mdi-refresh</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>리프레시 토큰</v-list-item-title>
                  <v-list-item-subtitle>{{ refreshTokenMasked }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        
        <v-card elevation="2">
          <v-card-title>
            <v-icon left color="primary">mdi-history</v-icon>
            최근 로그인 기록
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="loginHistoryHeaders"
              :items="loginHistory"
              :items-per-page="5"
              class="elevation-0"
            >
              <template #item.device="{ item }">
                <v-icon left :color="getDeviceColor(item.device)">{{ getDeviceIcon(item.device) }}</v-icon>
                {{ item.device }}
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
  name: 'ProfilePage',
  
  setup() {
    const authStore = useAuthStore();
    
    // 사용자 정보
    const userId = ref(authStore.user?.id || 1);
    const userName = ref(authStore.user?.username || '사용자');
    const userEmail = ref(authStore.user?.email || 'user@example.com');
    const userAvatar = computed(() => {
      return authStore.user?.imageUrl || 'https://via.placeholder.com/150?text=User';
    });
    
    // 계정 정보
    const joinDate = ref('2025-01-15');
    const lastLogin = ref('2025-04-16 15:30:45');
    
    // 토큰 정보
    const accessToken = localStorage.getItem('access_token') || '';
    const refreshToken = localStorage.getItem('refresh_token') || '';
    
    const maskToken = (token: string) => {
      if (!token) return '토큰 없음';
      return token.substring(0, 10) + '...' + token.substring(token.length - 5);
    };
    
    const accessTokenMasked = computed(() => maskToken(accessToken));
    const refreshTokenMasked = computed(() => maskToken(refreshToken));
    
    // 로그인 기록
    const loginHistoryHeaders = [
      { title: '날짜', key: 'date' },
      { title: 'IP 주소', key: 'ip' },
      { title: '장치', key: 'device' },
      { title: '위치', key: 'location' }
    ];
    
    const loginHistory = [
      {
        date: '2025-04-16 15:30:45',
        ip: '192.168.1.1',
        device: '데스크톱 (Windows)',
        location: '서울, 대한민국'
      },
      {
        date: '2025-04-15 10:22:15',
        ip: '192.168.1.1',
        device: '모바일 (Android)',
        location: '서울, 대한민국'
      },
      {
        date: '2025-04-14 18:45:30',
        ip: '192.168.1.1',
        device: '데스크톱 (Windows)',
        location: '서울, 대한민국'
      },
      {
        date: '2025-04-12 09:15:10',
        ip: '192.168.1.1',
        device: '태블릿 (iPad)',
        location: '서울, 대한민국'
      },
      {
        date: '2025-04-10 14:05:22',
        ip: '192.168.1.1',
        device: '데스크톱 (Windows)',
        location: '서울, 대한민국'
      }
    ];
    
    const getDeviceIcon = (device: string) => {
      if (device.includes('데스크톱')) return 'mdi-desktop-classic';
      if (device.includes('모바일')) return 'mdi-cellphone';
      if (device.includes('태블릿')) return 'mdi-tablet';
      return 'mdi-laptop';
    };
    
    const getDeviceColor = (device: string) => {
      if (device.includes('데스크톱')) return 'primary';
      if (device.includes('모바일')) return 'success';
      if (device.includes('태블릿')) return 'info';
      return 'grey';
    };
    
    return {
      userId,
      userName,
      userEmail,
      userAvatar,
      joinDate,
      lastLogin,
      accessTokenMasked,
      refreshTokenMasked,
      loginHistoryHeaders,
      loginHistory,
      getDeviceIcon,
      getDeviceColor
    };
  }
});
</script>

<style scoped>
.v-avatar {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
