<template>
  <v-app-bar app elevation="1" class="app-bar" color="primary">
    <div class="d-flex align-center justify-space-between w-100">
      <v-app-bar-nav-icon @click="$emit('toggle-drawer')"></v-app-bar-nav-icon>
      <div class="search-container mx-auto">
        <v-text-field
          density="compact"
          variant="solo"
          prepend-inner-icon="mdi-magnify"
          placeholder="Search"
          hide-details
          rounded="lg"
          color="white"
          class="search-field"
        ></v-text-field>
      </div>

      <div class="d-flex align-center">
        <v-btn icon class="mr-2">
          <v-icon>mdi-calendar-blank-outline</v-icon>
        </v-btn>
        
        <v-btn icon class="mr-2">
          <v-icon>mdi-cog-outline</v-icon>
        </v-btn>
        
        <v-btn icon class="mr-2">
          <v-icon>mdi-bell-outline</v-icon>
        </v-btn>

        <v-btn
          v-if="!isAuthenticated"
          color="primary"
          rounded="lg"
          class="login-btn"
          @click="login"
        >
          Log In
        </v-btn>
        
        <v-btn
          v-if="isAuthenticated"
          color="secondary"
          class="ml-2"
          @click="logout"
          variant="elevated"
          rounded="pill"
        >
          <v-icon left>mdi-logout</v-icon>
          로그아웃
        </v-btn>
        
        <v-menu
          left
          bottom
          offset-y
        >
          <template v-slot:activator="{ props }">
            <v-btn
              icon
              v-bind="props"
              variant="text"
            >
              <v-avatar size="36">
                <v-img
                  :src="userAvatar"
                  alt="User"
                ></v-img>
              </v-avatar>
            </v-btn>
          </template>

          <v-list>
            <v-list-item
              v-for="(item, index) in profileItems"
              :key="index"
              :to="item.to"
              link
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
            
            <v-divider></v-divider>
            
            <v-list-item @click="logout">
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
              
              <v-list-item-title>로그아웃</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'DashboardAppBar',
  
  emits: ['toggle-drawer'],
  
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    
    const isAuthenticated = computed(() => authStore.isAuthenticated);
    
    const userAvatar = computed(() => {
      return authStore.user?.imageUrl || 'https://via.placeholder.com/36?text=User';
    });
    
    const profileItems = [
      { title: '프로필', icon: 'mdi-account', to: '/dashboard/profile' },
      { title: '설정', icon: 'mdi-cog', to: '/dashboard/settings' },
    ];
    
    const login = () => {
      // 홈 페이지로 이동하여 로그인 화면 표시
      router.push('/');
    };
    
    const logout = () => {
      // 로컬 스토리지에서 데이터 제거
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      
      // 상태 초기화
      authStore.user = null;
      authStore.isAuthenticated = false;
      
      // 홈 페이지로 이동
      router.push('/');
    };
    
    return {
      isAuthenticated,
      userAvatar,
      profileItems,
      login,
      logout
    };
  }
});
</script>

<style scoped>
.app-bar {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.v-btn:hover, .v-btn:focus {
  background-color: #fff !important;
  color: #535C91 !important; /* primary color */
}


.search-container {
  max-width: 400px;
  width: 100%;
}

.search-field {
  max-width: 400px;
}

.login-btn {
  background-color: var(--color-secondary) !important;
  color: white;
  font-weight: 500;
  padding: 0 20px;
}
</style>
