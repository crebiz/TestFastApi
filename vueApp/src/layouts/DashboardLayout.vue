<template>
  <v-app>
    <Sidebar v-model:drawer="drawer" />
    <AppBar :title="currentRouteName" @toggle-drawer="drawer = !drawer" />
    
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
  background-color: #f5f5f5;
}
</style>
