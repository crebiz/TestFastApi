<template>
  <v-footer
    app
    padless
    class="font-weight-medium"
  >
    <v-container>
      <v-row
        no-gutters
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          md="auto"
          class="text-center text-md-left"
        >
          &copy; {{ new Date().getFullYear() }} — <strong>Crebiz Community</strong>
        </v-col>
        <v-spacer class="d-none d-md-block"></v-spacer>
        <v-col
          cols="12"
          md="auto"
          class="text-center text-md-right"
        >
          <v-btn
            v-for="link in links"
            :key="link.name"
            text
            small
            class="mx-1"
            :href="link.href"
            target="_blank"
          >
            {{ link.name }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppFooter',
  
  setup() {
    const links = [
      { name: '홈', href: '/' },
      { name: '서비스', href: '#' },
      { name: '회사 소개', href: '#' },
      { name: '문의하기', href: '#' },
    ];
    
    return {
      links
    };
  }
});
</script>

<style scoped>
.v-footer {
  border-top: 1px solid #eee;
}
</style>
