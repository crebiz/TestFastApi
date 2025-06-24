<template>
  <v-navigation-drawer :model-value="drawer" @update:model-value="$emit('update:drawer', $event)"
    :mini-variant="miniVariant" :clipped="false" app class="sidebar-aligned" elevation="1"
    color="primary">
    
    <div class="d-flex align-center pa-4">
      <v-toolbar-title class="font-weight-bold ml-2">CrebizCommunity</v-toolbar-title>
    </div>
    
    <v-divider></v-divider>

    <v-list nav density="compact" class="pa-2">
      <v-list-item 
        v-for="item in items" 
        :key="item.title" 
        :to="item.to" 
        :exact="item.exact" 
        link 
        rounded="lg"
        :active-class="'active-item'" 
        class="mb-1">
        <template v-slot:prepend>
          <v-icon class="me-2">{{ item.icon }}</v-icon>
        </template>
        {{ item.title }}
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-4 d-flex flex-column">
        <v-btn variant="text" block prepend-icon="mdi-help-circle-outline" class="text-left mb-2">
          Help
        </v-btn>
        <div class="d-flex align-center justify-space-between">
          <span class="text-caption">테마 변경</span>
          <ThemeSwitcher />
        </div>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import ThemeSwitcher from '../ThemeSwitcher.vue';

export default defineComponent({
  name: 'DashboardSidebar',
  components: {
    ThemeSwitcher
  },

  props: {
    drawer: {
      type: Boolean,
      default: true
    }
  },

  emits: ['update:drawer'],

  setup(props, { emit }) {
    // drawer는 템플릿에서 직접 props 사용
    const miniVariant = ref(false);
    const clipped = ref(true);

    const toggleDrawer = () => {
      emit('update:drawer', !props.drawer);
    };

    const items = [
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard', exact: true },
      { title: 'Login Info', icon: 'mdi-account', to: '/dashboard/profile', exact: false },
      { title: 'Budget', icon: 'mdi-scale-balance', to: '/dashboard/budget', exact: false },
      { title: 'Fund', icon: 'mdi-cash-multiple', to: '/dashboard/fund', exact: false },
      { title: 'Card', icon: 'mdi-card-bulleted', to: '/dashboard/card', exact: false },
      { title: 'Code', icon: 'mdi-code-brackets', to: '/dashboard/code', exact: false },
      { title: 'Flow', icon: 'mdi-graph-outline', to: '/dashboard/flow', exact: false },
      { title: 'Tab', icon: 'mdi-tab', to: '/dashboard/tab', exact: false },
    ];

    return {
      miniVariant,
      clipped,
      toggleDrawer,
      items,
    };
  }
});
</script>

<style scoped>
.v-list-item {
  font-weight: 500;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.v-list-item:hover, .v-list-item:focus {
  background-color: #fff !important;
  color: #535C91 !important; /* primary color */
}


.v-list-item .v-icon {
  margin-right: 8px;
}

.active-item {
  color: white;
}

.v-navigation-drawer {
  border-right: none !important;
}
</style>
