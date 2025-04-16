<template>
  <v-navigation-drawer 
    :model-value="drawer" 
    @update:model-value="$emit('update:drawer', $event)"
    :mini-variant="miniVariant" 
    :clipped="false" 
    app 
    color="primary" 
    dark
    class="sidebar-aligned"
    floating
    elevation="3"
    rounded="lg"
  >
    <v-list-item class="px-2">
      <v-list-item-avatar>
        <v-img src="https://via.placeholder.com/50?text=CC" alt="Crebiz Community"></v-img>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title class="text-h6">
          Crebiz Community
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense nav>
      <v-list-item v-for="item in items" :key="item.title" :to="item.to" link>
        <template v-slot:prepend>
          <v-icon class="me-2">{{ item.icon }}</v-icon>
        </template>
        {{ item.title }}
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'DashboardSidebar',

  props: {
    drawer: {
      type: Boolean,
      default: true
    }
  },

  emits: ['update:drawer'],

  setup() {
    // drawer는 템플릿에서 직접 props 사용
    const miniVariant = ref(false);
    const clipped = ref(true);

    const items = [
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
      { title: 'Login Info', icon: 'mdi-account', to: '/dashboard/profile' },
      { title: 'Fund', icon: 'mdi-cash-multiple', to: '/dashboard/fund' },
    ];

    return {
      miniVariant,
      clipped,
      items
    };
  }
});
</script>

<style scoped>
.v-list-item {
  font-weight: 500;
  display: flex;
  align-items: center;
}

.v-list-item .v-icon {
  margin-right: 8px;
}

/* AppBar와 높이 맞추기 */
.v-navigation-drawer {
  top: 64px !important; /* 기본 AppBar 높이 */
  max-height: calc(100% - 64px) !important;
  height: calc(100% - 64px) !important;
  z-index: 1; /* AppBar보다 낮은 z-index */
  border-radius: 0 16px 0 0 !important; /* Material Design 3 스타일 */
  margin-top: 4px;
}
</style>
