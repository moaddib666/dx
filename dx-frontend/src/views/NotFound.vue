<template>
  <div class="page-container">
    <div class="hero-background"></div>
    <main class="not-found">
      <TitleComponent>{{ t('notFound.title') }}</TitleComponent>
      <div class="not-found-content">
        <p>{{ t('notFound.message') }}</p>
      </div>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'NotFound',
  components: {
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
  background-image: url('@/assets/images/backgrounds/dx-background-jonnie-404.png');
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

.not-found {
  padding: 60px;
  color: white;
  position: relative;
  z-index: 1;
}

.not-found-content {
  margin-top: 2rem;
  font-size: 1.2rem;
  line-height: 1.6;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}
</style>