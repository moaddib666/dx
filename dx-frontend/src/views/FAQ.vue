<template>
  <div class="page-container">
    <div class="hero-background"></div>
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
.page-container {
  position: relative;
}

.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/backgrounds/generic-background.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

.faq {
  padding: 60px;
  color: white;
  position: relative;
  z-index: 1;
}
</style>
