<template>
  <v-app>
    <AppBar :title="currentRouteName" @toggle-drawer="drawer = !drawer" />
    <Sidebar v-model:drawer="drawer" />
    
    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
    
    <AppFooter />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import AppBar from '@/components/dashboard/AppBar.vue';
import AppFooter from '@/components/dashboard/AppFooter.vue';

export default defineComponent({
  name: 'DashboardLayout',
  
  components: {
    Sidebar,
    AppBar,
    AppFooter
  },
  
  setup() {
    const drawer = ref(true);
    const route = useRoute();
    
    const currentRouteName = computed(() => {
      const name = route.name?.toString() || '';
      return name.charAt(0).toUpperCase() + name.slice(1);
    });
    
    return {
      drawer,
      currentRouteName
    };
  }
});
</script>

<style scoped>
.v-main {
  background-color: #E0F2F1; /* Light Teal 배경색 */
  padding-top: 64px !important; /* AppBar 높이와 동일하게 설정 */
}

.v-container {
  padding: 16px;
  max-width: 1440px;
}

/* Material Design 3 스타일 */
.v-card {
  border-radius: 16px !important;
  overflow: hidden;
}
</style>
