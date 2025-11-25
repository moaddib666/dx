<template>
  <div class="page-container">
    <div class="hero-background"></div>
    <main class="faq">
      <TitleComponent>{{ t('faq.title') }}</TitleComponent>
      <p class="faq-description">{{ t('faq.description') }}</p>
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
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
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
  max-width: 1200px;
  width: 100%;
  padding: 3rem 2rem;
  color: #e0f7fa;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  margin: 0 auto;
  border-radius: 12px;
}

.faq-description {
  font-size: 1.2rem;
  line-height: 1.7;
  color: #b0e7f0;
  text-align: center;
  margin-bottom: 2.5rem;
  margin-top: 1rem;
  font-weight: 400;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 1024px) {
  .faq {
    max-width: 100%;
    padding: 2.5rem 1.5rem;
    padding-top: 80px;
  }

  .faq-description {
    font-size: 1.15rem;
    margin-bottom: 2rem;
  }
}

@media (max-width: 768px) {
  .faq {
    padding: 2rem 1.25rem;
    padding-top: 70px;
  }

  .faq-description {
    font-size: 1.1rem;
    margin-bottom: 1.75rem;
  }
}

@media (max-width: 480px) {
  .faq {
    padding: 1.5rem 1rem;
    padding-top: 60px;
  }

  .faq-description {
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
  }
}
</style>
