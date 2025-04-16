<template>
  <v-app-bar
    app
    color="white"
    flat
    elevation="1"
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
    
    <v-menu
      left
      bottom
      offset-y
    >
      <template v-slot:activator="{ props }">
        <v-btn
          icon
          v-bind="props"
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
    
    const userAvatar = computed(() => {
      return authStore.user?.imageUrl || 'https://via.placeholder.com/36?text=User';
    });
    
    const profileItems = [
      { title: '프로필', icon: 'mdi-account', to: '/dashboard/profile' },
      { title: '설정', icon: 'mdi-cog', to: '/dashboard/settings' },
    ];
    
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
      userAvatar,
      profileItems,
      logout
    };
  }
});
</script>

<style scoped>
.v-app-bar {
  border-bottom: 1px solid #eee;
}
</style>
