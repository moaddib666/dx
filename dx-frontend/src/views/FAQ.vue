<template>
  <div>
    <main class="faq">
      <TitleComponent>{{ t('faq.title') }}</TitleComponent>
      <p>{{ t('faq.description') }}</p>
      <f-a-q></f-a-q>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import FAQ from '@/components/FAQ.vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    FAQ,
    TitleComponent
  },
  setup() {
    const { t } = useI18n();
    return { t };
  }
};
</script>

<style scoped>
.faq {
  padding: 60px;
  color: white;
}
</style>
