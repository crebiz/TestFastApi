<template>
  <v-app-bar
    app
    color="primary"
    dark
    elevation="2"
    height="64"
    class="app-bar-fixed"
    rounded="0"
  >
    <v-app-bar-nav-icon @click.stop="$emit('toggle-drawer')"></v-app-bar-nav-icon>
    
    <v-toolbar-title class="ml-2">{{ title }}</v-toolbar-title>
    
    <v-spacer></v-spacer>
    
    <v-btn icon>
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
    
    <v-btn icon>
      <v-icon>mdi-bell</v-icon>
    </v-btn>
    
    <!-- 로그인 상태에 따라 버튼 표시 -->
    <v-btn
      v-if="!isAuthenticated"
      color="secondary"
      class="ml-2"
      @click="login"
      variant="elevated"
      rounded="pill"
    >
      <v-icon left>mdi-google</v-icon>
      구글 로그인
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
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useAuthStore } from '../../stores/authStore';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'DashboardAppBar',
  
  props: {
    title: {
      type: String,
      default: 'Dashboard'
    }
  },
  
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
.v-app-bar {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.app-bar-fixed {
  z-index: 5; /* Sidebar보다 높은 z-index */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.v-btn.v-btn--variant-elevated {
  background-color: var(--v-theme-secondary) !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-weight: 500;
  box-shadow: 0 3px 5px -1px rgba(0,0,0,.2),0 6px 10px 0 rgba(0,0,0,.14),0 1px 18px 0 rgba(0,0,0,.12);
}

.v-toolbar-title {
  font-weight: 500;
  letter-spacing: 0.0125em;
}

/* Material Design 3 스타일 */
.v-btn--icon {
  border-radius: 50%;
  min-width: 36px;
  width: 36px;
  height: 36px;
  margin: 0 4px;
}
</style>
