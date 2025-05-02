<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    location="right"
    temporary
    width="520"
    class="detail-drawer"
    elevation="24"
  >
    <v-card flat class="h-100" style="border-radius: 0">
      <v-toolbar flat :color="headerColor" dark class="pa-3">
        <v-toolbar-title class="text-h6 font-weight-medium ml-2 text-truncate">
          {{ title }}
        </v-toolbar-title>
        <v-btn icon @click="$emit('update:modelValue', false)" class="mr-2">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-6">
        <slot></slot>
      </v-card-text>
    </v-card>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: '상세 정보'
  },
  headerColor: {
    type: String,
    default: 'primary'
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.detail-drawer {
  z-index: 1000;
}
</style>
