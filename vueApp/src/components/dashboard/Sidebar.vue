<template>
  <v-navigation-drawer
    v-model="drawer"
    :mini-variant="miniVariant"
    :clipped="clipped"
    app
    color="primary"
    dark
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

      <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>{{ miniVariant ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
      </v-btn>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense nav>
      <v-list-item
        v-for="item in items"
        :key="item.title"
        :to="item.to"
        link
      >
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'DashboardSidebar',
  
  setup() {
    const drawer = ref(true);
    const miniVariant = ref(false);
    const clipped = ref(true);
    
    const items = [
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
      { title: 'Login Info', icon: 'mdi-account', to: '/dashboard/profile' },
      { title: 'Fund', icon: 'mdi-cash-multiple', to: '/dashboard/fund' },
    ];
    
    return {
      drawer,
      miniVariant,
      clipped,
      items
    };
  }
});
</script>

<style scoped>
.v-list-item__title {
  font-weight: 500;
}
</style>
